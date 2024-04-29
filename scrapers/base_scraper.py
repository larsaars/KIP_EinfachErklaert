#!/usr/bin/env python3

"""
Base scraper interface and some utility funcitons. Takes care of basic functioning and provides a skeleton for scrapers.
"""

import sys

# add parent dir to the python path to enable importing services module (and by that DataHandler)
sys.path.append('..')

from services.DataHandler import DataHandler
from bs4 import BeautifulSoup
import requests


def base_metadata_dict():
    """
    Returns a dictionary with the basic metadata fields.
    """

    return {
        'title': None,
        'description': None,
        'kicker': None,
        'date': None, 
        'url': None,
        'image_url': None,
        'image_description': None,
        'audio': None,
        'match': None,
    }

def base_audio_dict():
    """
    Returns a dictionary with the basic audio metadata fields.
    """
    return {
        'audio_url': None,
        'download_url': None,
        'duration': None,
    }


class BaseScraper:
    def __init__(self, feed_url, data_handler_source=None):
        """
        Initialize the BaseScraper.

        Args:
            feed_url (str): url of the page to scrape
            data_handler_source (str): source of the data handler
        """

        self.feed_url = feed_url
        self.feed_soup = self._get_soup(feed_url)
        self.data_handler = DataHandler(data_handler_source)

    def _get_soup(self, url):
        """
        Get the soup object of the url.

        Args:
            url (str): url of the page to scrape

        Returns:
            BeautifulSoup: soup object of the url
        """

        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
        return BeautifulSoup(response.text, 'html.parser')

    def _fetch_articles_from_feed(self) -> list:
        """
        Fetches the articles from the feed.

        Returns:
            list: list of article urls
        """

        pass

    def _get_metadata_and_content(self, url):
        """
        Get the metadata and content of the article.

        Args:
            url (str): url of the article
        """

        pass

    def scrape(self):
        """
        Scrape the page and save the data to the database.
        """
        pass



if __name__ == '__main__':
    pass  # do testing

