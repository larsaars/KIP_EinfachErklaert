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


def get_soup(url):
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
        'audio': None
    }


class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.data_handler = DataHandler()
        self.soup = get_soup(url)



if __name__ == '__main__':
    pass # do testing

