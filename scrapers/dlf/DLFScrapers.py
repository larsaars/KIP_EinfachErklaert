#!/usr/bin/env python3

"""
Class Definitions of DeutschlandradioScraper, DeutschlandfunkScraper and NachrichtenleichtScraper.
"""

import sys
import os
import logging
import sys
import subprocess

# add git root dir to the python path to enable importing services modules
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

from datahandler.DataHandler import DataHandler

from scrapers.base.base_scraper import BaseScraper, base_metadata_dict, base_audio_dict
from bs4 import BeautifulSoup
from datetime import datetime

dsf_feed_url = "https://www.deutschlandfunk.de/nachrichten-100.html"
nl_feed_url  = "https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems=0&drsearch:itemsPerLoad=30&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1"



class DeutschlandradioScraper(BaseScraper):
    def __init__(self, feed_url, difficulty):
        super().__init__(feed_url, "dlf")
        self.difficulty_level = difficulty

    def _fetch_articles_from_feed(self) -> list:
        articles = []
        for feed_article in self.feed_soup.find_all("article"):
            try:
                articles.append(feed_article.find("a")["href"])
            except Exception:
                continue
        return articles

    def _get_metadata_and_content(self, url) -> tuple:
        """
        Get the content, metadata and html of the article.
        Returns content, metadata dictionary and the raw html.
        """
        html    = self._get_soup(url)
        article = html.find("article", class_="b-article")
        self.article = article
        content  = get_article_content(article)
        metadata = base_metadata_dict()
        
        metadata["url"]    = url
        metadata["title"]  = find_string(article, class_="headline-title")
        metadata["kicker"] = find_string(article, class_="headline-kicker")
        date_str           = find_string(article, class_="article-header-author")
        metadata["date"]   = datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        metadata["description"] = find_string(article, class_="article-header-description")
        metadata["image_description"] = find_string(article, "figcaption")

        try:
            metadata["image_url"] = article.find("img")["src"]
        except Exception:
            pass

        return content, metadata, str(html)

    def scrape(self) -> list:
        for article_url in self._fetch_articles_from_feed():
            if not self.data_handler.is_already_saved(self.difficulty_level, article_url):
                content, metadata, html = self._get_metadata_and_content(article_url)
                content = "\n".join(content)
                self.data_handler.save_article(self.difficulty_level, metadata, content, html, download_audio=True)


class DeutschlandfunkScraper(DeutschlandradioScraper):
    def __init__(self):
        super().__init__(dsf_feed_url, "hard")


class NachrichtenleichtScraper(DeutschlandradioScraper):
    def __init__(self):
        super().__init__(nl_feed_url, "easy")

    def _get_audio_metadata(self, article) -> dict:
        data = None
        try:
            audio = article.find(class_="js-audio")
        except Exception:
            return None
        if audio:
            data = base_audio_dict()
            data["audio_url"]    = audio["href"]
            data["download_url"] = audio["data-audio-download-src"]
            data["duration"]     = audio["data-audioduration"]
        return data
        

    def _get_metadata_and_content(self, url) -> tuple:
        """
        Get the content, metadata and html of the article.
        Returns content, metadata dictionary and the raw html.
        """
        content, metadata, html = super()._get_metadata_and_content(url)
        metadata["audio"]  = self._get_audio_metadata(self.article)

        return content, metadata, html


def get_article_content(article_soup) -> list:
    """
    Extracts the article content and returns a list of paragraphs.
    """
    content = []
    for section in article_soup.find(class_="b-article-details").children:
        if section.name == "h2":
            content.append(section.text)
        if section.name == "div":
            content.append(section.text)
    return content

def find_string(article, *args, **kwargs):
    """
    Secure version of the bs4 function find().string.
    """
    try:
        content = article.find(*args, **kwargs).string
    except Exception:
        content = None
    return content