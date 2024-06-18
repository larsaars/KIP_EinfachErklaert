#!/usr/bin/env python3

import logging
import requests
import sys
import os

from mdr_base import MDRBaseScraper
from matchers.SimpleMatcher import SimpleMatcher

"""Scrapes the historic easy and hard articles of MDR with the help of previously scraped links on top of the 
MDRBaseScraper class"""


class MDRHistoricScraper(MDRBaseScraper):
    def __init__(self, easy_article_urls: list):
        super().__init__()

        self.easy_article_urls = easy_article_urls

        # create a simple matcher object
        self.matcher = SimpleMatcher('mdr')

    def scrape(self):
        """
        Scrapes the previously scraped easy article links from the MDR website.
        Only if an easy article finds a hard match, the both articles are scraped.
        """

        logging.info('Starting to scrape historic MDR articles.')

        for easy_article_url in self.easy_article_urls:
            # strip newline characters
            easy_article_url = easy_article_url.strip()

            logging.info(f'Scraping easy article: {easy_article_url}')

            # get the metadata, content and html
            try:
                easy_metadata, easy_content, easy_html = self._get_easy_article_metadata_and_content(easy_article_url)
            except Exception as e:
                logging.error(f'Error while scraping easy article: {e}')
                continue

            # get the hard article url from the easy article metadata
            hard_article_url = easy_metadata['match']

            # save the article to the database
            # returns True if the article is newly scraped
            newly_scraped = self.data_handler.save_article('easy', easy_metadata, easy_content, easy_html,
                                                           download_audio=True)

            # if no hard match has been found, skip scraping hard article
            # but still save easy article
            if hard_article_url is None:
                continue

            # strip hard article url
            hard_article_url = hard_article_url.strip()

            # scrape hard article
            logging.info(f'Scraping the hard article: {hard_article_url}')

            try:
                hard_metadata, hard_content, hard_html = self._get_hard_article_metadata_and_content(hard_article_url)
            except Exception as e:
                logging.error(f'Error while scraping hard article: {e}')
                continue

            # write the match url string in hard article metadata
            hard_metadata['match'] = easy_article_url

            # save the hard article to the database
            # if one of the articles is newly scraped, the match is newly scraped
            newly_scraped = self.data_handler.save_article('hard', hard_metadata, hard_content, hard_html,
                                                           download_audio=True) or newly_scraped

            # match the articles via simple matcher function
            # if newly scraped (prevents from duplicate match writing)
            if newly_scraped:
                self.matcher.match_by_url(easy_article_url, hard_article_url)


if __name__ == '__main__':
    # scrape historic MDR articles
    # the links have been scraped before and are stored in a local file
    # the file is read and the links are scraped

    # the filename of the file with easy article urls is passed as an argument to the scraper
    # get this filename from the command line arguments
    if len(sys.argv) != 2:
        logging.error('Please provide the filename of the file with easy article urls.')
        sys.exit(1)
    else:
        easy_article_urls_filename = sys.argv[1]

    # read the file with the easy article urls
    with open(easy_article_urls_filename, 'r') as file:
        easy_article_urls = file.readlines()

    try:
        MDRHistoricScraper(easy_article_urls).scrape()
        # don't ignore keyboard interrupts by other exceptions
    except KeyboardInterrupt:
        logging.info('Interrupted by user.')
        sys.exit(0)
