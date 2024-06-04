#!/usr/bin/env python3

import logging
import requests
import sys
from mdr_base import MDRBaseScraper

from matchers.SimpleMatcher import SimpleMatcher

"""Scrapes the historic easy and hard articles of MDR with the help of bing search API on top of the MDRBaseScraper class"""
class MDRHistoricScraper(MDRBaseScraper):
    def __init__(self): 
        super().__init__()

        # create a simple matcher object
        self.matcher = SimpleMatcher('mdr')


    def _get_next_api_results(self) -> bool:
        """Uses the bing search API to get the next results.
        (Searching for
        intext:"Hier können Sie diese Nachricht auch in schwerer Sprache lesen:" site:mdr.de
        which ensures that a hard article match is for sure inside.)
        Saves urls to be scraped in class varible self._api_results.


        Returns:
            bool: True if there are more results, False otherwise
        """

        # TODO

        return BOOL TODO

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
                try:
                    easy_metadata, easy_content, easy_html = self._get_easy_article_metadata_and_content(easy_article_url)
                except Exception as e:
                    logging.error(f'Error while scraping easy article: {e}')
                    continue

                hard_article_url = easy_metadata['match']


                # save the article to the database
                # returns True if the article is newly scraped
                newly_scraped = self.data_handler.save_article('easy', easy_metadata, easy_content, easy_html, download_audio=True)

                # if no hard match has been found, skip scraping hard article
                # but still save easy article
                if hard_article_url == None:
                    continue

                # scrape hard article
                logging.info(f'Scraping the hard article: {hard_article_url}')

                try:
                    hard_metadata, hard_content, hard_html = self._get_hard_article_metadata_and_content(hard_article_url)
                except Exception as e:
                    logging.error(f'Error while scraping hard article: {e}')
                    continue


                # write the match url string in hard article metadata
                hard_metadata['match'] =  easy_article_url

                # save the hard article to the database
                # if one of the articles is newly scraped, the match is newly scraped
                newly_scraped = newly_scraped or self.data_handler.save_article('hard', hard_metadata, hard_content, hard_html, download_audio=True)


                # match the articles via simple matcher function
                # if newly scraped (prevents from duplicate match writing)
                if newly_scraped:
                    self.matcher.match_by_url(easy_article_url, hard_article_url)



if __name__ == '__main__':
    # scrape current MDR articles
    try:
        MDRHistoricScraper().scrape()
        # don't ignore keyboard interrupts by other exceptions
    except KeyboardInterrupt:
        logging.info('Interrupted by user.')
        sys.exit(0)


