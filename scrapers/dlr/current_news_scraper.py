#!/usr/bin/env python3

"""
Scrapes the current articles from Deutschlandfunk and Nachrichtenleicht and saves them to the database.
"""

import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)
from services.DataHandler import DataHandler

from scrapers.base_scraper import BaseScraper, base_metadata_dict, base_audio_dict
from bs4 import BeautifulSoup

dsf_feed_url = "https://www.deutschlandfunk.de/nachrichten-100.html"
nl_feed_url  = "https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems=0&drsearch:itemsPerLoad=30&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1"


class DeutschlandfunkScraper(BaseScraper):
    def __init__(self):
        super().__init__(dsf_feed_url, "dlf")

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
        Get the metadata and content of the article.
        Returns content and metadata dictionary.
        """
        article = self._get_soup(url).find("article", class_="b-article")

        content  = get_article_content(article)
        metadata = base_metadata_dict()
        
        metadata["url"]    = url
        metadata["title"]  = find_string(article, class_="headline-title")
        metadata["kicker"] = find_string(article, class_="headline-kicker")
        metadata["date"]   = find_string(article, class_="article-header-author")
        metadata["description"] = find_string(article, class_="article-header-description")
        metadata["image_description"] = find_string(article, "figcaption")

        try:
            metadata["image_url"] = article.find("img")["src"]
        except Exception:
            pass

        return content, metadata

    def scrape(self) -> list:
        for article_url in self._fetch_articles_from_feed():
            if not self.data_handler.is_already_saved("hard", article_url):
                content, metadata = self._get_metadata_and_content(article_url)
                content = "\n".join(content)
                self.data_handler.save_article('hard', metadata, content, download_audio=False)

class NachrichtenleichtScraper(BaseScraper):
    def __init__(self):
        super().__init__(nl_feed_url, "dlf")

    def _fetch_articles_from_feed(self) -> list:
        articles = []
        for feed_article in self.feed_soup.find_all("article"):
            try:
                articles.append(feed_article.find("a")["href"])
            except Exception:
                continue
        return articles

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
        Get the metadata and content of the article.
        Returns content and metadata dictionary.
        """
        article = self._get_soup(url).find("article", class_="b-article")

        content  = get_article_content(article)
        metadata = base_metadata_dict()
        
        metadata["url"]    = url
        metadata["title"]  = find_string(article, class_="article-header-title")
        metadata["kicker"] = find_string(article, class_="headline-kicker")
        metadata["date"]   = find_string(article, class_="article-header-author")
        metadata["description"] = find_string(article, class_="article-header-description")
        metadata["image_description"] = find_string(article, "figcaption")
        metadata["audio"]  = self._get_audio_metadata(article)

        try:
            metadata["image_url"] = article.find("img")["src"]
        except Exception:
            pass

        return content, metadata

    def scrape(self) -> list:
        for article_url in self._fetch_articles_from_feed():
            if not self.data_handler.is_already_safed("easy", article_url):
                content, metadata = self._get_metadata_and_content(article_url)
                content = "\n".join(content)
                self.data_handler.save_article('easy', metadata, content, download_audio=False)

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

if __name__ == '__main__':
    DeutschlandfunkScraper().scrape()
    NachrichtenleichtScraper().scrape()
