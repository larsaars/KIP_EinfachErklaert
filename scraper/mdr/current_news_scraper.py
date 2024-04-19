#!/usr/bin/env python3

"""
Scrapes the current articles from WDR (easy & hard language) and saves them to the database.
"""

import sys

# add parent dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append('../..')

from scraper.base_scraper import BaseScraper, base_metadata_dict
from bs4 import BeautifulSoup

class MDREasyScraper(BaseScraper):
    def __init__(self):
        # init with feed url and source
        super().__init__('https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html', 'mdr')

    def _fetch_articles_from_feed(self) -> list:
        """
        Fetches the articles from the feed.

        Returns:
            list: list of article urls
        """

        base_url = 'https://www.mdr.de'  # base url of the articles since the links are relative
        articles = []  # list of articles to be returned

        # the links are wrapped within a div per day
        for day_div in self.feed_soup.find_all('div', class_='linklist cssBoxTeaserLink'):
            # get the links
            for link in day_div.find_all('a'):
                # append the base url to the relative link
                articles.append(base_url + link['href'])

        return articles

    def _get_metadata_and_content(self, url):
        """
        Get the metadata and content of the article.

        Args:
            url (str): url of the article

        Returns:
            dict: metadata of the article
        """

        metadata = base_metadata_dict()  # metadata dict to be returned
        soup = self._get_soup(url)  # get the soup object of the article

        paragraphs = soup.find_all('div', class_='paragraph')  # get the article paragraphs
        del paragraphs[-1]  # delete last paragraph since it contains unwanted information

        content = ''

        # edit each paragraph to remove the unwanted tags and build content string
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.find('p')

            for tag in paragraph.find_all(['a']):
                del tag['data-ctrl-link']  # all links have this attribute which is not needed
            
            paragraph_text = ''.join([str(c) for c in paragraph.contents])  # stringify the content of the paragraph 

            # add the paragraph to the content string
            content += paragraph_text

            # if it is the first paragraph, use as description
            if i == 0:
                metadata['description'] = paragraph_text



        # fill the base metadata dict
        metadata['url'] = url  # source url
        metadata['title'] = soup.find('span', class_='headline').text  # title
        metadata['kicker'] = soup.find('span', class_='dachzeile').text  # kicker
        metadata['date'] = soup.find('p', class_='webtime').text  # date (not nicely formatted)

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            pass

        # TODO AUDIO DOWNLOAD (is available, but has extracting is not that easy)

        metadata['match'] = ''  # an url to the hard version of the article is available! (TODO: extract it AND
        # TODO this also contains the hard article's audio link in a second xml')


        return content, metadata 

    def scrape(self) -> list:
        """
        Scrapes the articles from the feed and saves them to the database.

        Returns:
            list: list of dicts with easy and hard article urls
        """

        easy_and_hard_articles = []  # the list tb returned

        for article in self._fetch_articles_from_feed():
            content, metadata = self._get_metadata_and_content(article)
            # save the article to the database
            print(metadata)
            self.data_handler.save_article('easy', metadata, content, download_audio=True)
            # append to the list
            easy_and_hard_articles.append({
                'easy': metadata['url'],
                'hard': metadata['match']
            })

        return easy_and_hard_articles



if __name__ == '__main__':
    easy_and_hard_articles = MDREasyScraper().scrape()
    # TODO: MDRHardScraper(easy_and_hard_articles).scrape()
