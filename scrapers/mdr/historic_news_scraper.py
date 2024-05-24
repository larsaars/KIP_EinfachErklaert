#!/usr/bin/env python3

import sys
import os
import logging
import subprocess

from time import sleep
import requests
import json

from mdr_base import MDRBaseScraper
from bs4 import BeautifulSoup



"""Scrapes the historic easy and hard articles of MDR with the help of the search API on top of the MDRBaseScraper class"""
class MDRHistoricScraper(MDRBaseScraper):
    def __init__(self): 
        super().__init__()

        # init vars needed by _get_next_api_results
        self._api_results_start_index = 0

        # init white list of which link types are allowed
        self._api_white_list = [
            'nachrichten-leicht',
            'barrierefreiheit/leichte-sprache'
        ]

        # and a blacklist of which ones are filtered out after whitelisting
        # (working with contains)
        self._api_black_list = [
            'video',
            'audio',
            'woerterbuch',
            'spezial',
            'rueckblick'
        ]

    def _get_next_api_results(self) -> bool:
        """Uses the MDR search API to get the next results.
        (Searching for keywords "leichte sprache")
        Saves urls to be scraped in class varible self._api_results.

        Filters results that should not be scraped.
        (With first whitelist and then blacklist approach, allow only certain types of links,
        and then remove from the allowed links the blacklisted ones.)

        Returns:
            bool: True if there are more results, False otherwise
        """
        # clear the list of results
        self._api_results = []
        request_url = f'https://www.mdr.de/suche/suche--100-searchResults.json?changefilter=&filter=&q=leichte+sprache&rows=30&sort=time&start={self._api_results_start_index}'

        # request the search results
        try:
            response = requests.get(request_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f'Error while fetching search results: {e}')
            return False
        
        # parse the json response
        # and loop through searchResults list
        for result in response.json()['searchResults']:
            # get the url
            url = result['teaser']['url']

            # check if the url is in the whitelist
            if not any(allowed_link in url for allowed_link in self._api_white_list):
                continue

            # check if the url is in the blacklist
            if any(blacklisted_link in url for blacklisted_link in self._api_black_list):
                continue

            # append the url to the list of results
            self._api_results.append(url)

        # update api start index
        self._api_results_start_index += 30

        return self._api_results_start_index < 12000

    def scrape(self):
        """
        Uses the search API to scrape the easy articles from the MDR website.
        Only if an easy article finds a hard match, the both articles are scraped.
        """

        logging.info('Starting to scrape historic MDR articles.')

        # loop as long as there are next api results
        # the api results are in pages of 30 results
        # it does not allow loading more than 12000 results in total
        # (talking here not about articles, but results)
        while (self._get_next_api_results()):

            # loop through list of results
            for easy_article_url in self._api_results:

                logging.info(f'Scraping easy article: {easy_article_url}')

                # get the metadata, content and html
                easy_metadata, easy_content, easy_html = self._get_easy_article_metadata_and_content(easy_article_url)

                hard_article_url = easy_metadata['match']

                # if no hard match has been found, skip saving 
                # easy article and scraping hard
                if hard_article_url == None:
                    continue

                # save the article to the database
                self.data_handler.save_article('easy', easy_metadata, easy_content, easy_html, download_audio=True)


                # scrape hard article
                logging.info(f'Scraping the hard article: {hard_article_url}')

                hard_metadata, hard_content, hard_html = self._get_hard_article_metadata_and_content(hard_article_url)

                # write the match url string in hard article metadata
                hard_metadata['match'] =  easy_article_url

                # save the hard article to the database
                self.data_handler.save_article('hard', hard_metadata, hard_content, hard_html, download_audio=True)





if __name__ == '__main__':
    # scrape current MDR articles
    MDRHistoricScraper().scrape()

