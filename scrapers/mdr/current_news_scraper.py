#!/usr/bin/env python3

import logging

from time import sleep

from mdr_base import MDRBaseScraper
from bs4 import BeautifulSoup
from matchers.SimpleMatcher import SimpleMatcher



"""Scrapes the current easy and hard articles of MDR from easy language feed url on top of the MDRBaseScraper class"""
class MDRCurrentScraper(MDRBaseScraper):
    def __init__(self): 
        super().__init__()

        # init the soup object for the feed of the easy articles
        # a soup for the hard articles is not needed since
        # they are referred to by easy articles
        self._easy_feed_soup = self._get_soup('https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html')

        # create a simple matcher object
        self.matcher = SimpleMatcher('mdr')

    def _fetch_easy_articles_from_feed(self) -> list:
        """
        Fetches the easy articles from the feed.

        Returns:
            list: list of easy article urls
        """

        base_url = 'https://www.mdr.de'  # base url of the articles since the links are relative
        articles = []  # list of articles to be returned

        # the links are wrapped within a div per day
        for day_div in self._easy_feed_soup.find_all('div', class_='linklist cssBoxTeaserLink'):
            # get the links
            for link in day_div.find_all('a'):
                # append the base url to the relative link
                articles.append(base_url + link['href'])

        return articles


    def scrape(self):
        """
        Scrapes the articles from the easy articles feed as well as hard articles
        and saves them to the database.
        """

        logging.info('Starting to scrape current MDR articles.')

        for easy_article_url in self._fetch_easy_articles_from_feed():
            logging.info(f'Scraping easy article: {easy_article_url}')

        
            # get the metadata, content and html
            easy_metadata, easy_content, easy_html = self._get_easy_article_metadata_and_content(easy_article_url)
            # save the article to the database
            # returns True if the article is newly scraped
            newly_scraped = self.data_handler.save_article('easy', easy_metadata, easy_content, easy_html, download_audio=True)


            # with the match url get the hard language article
            hard_article_url = easy_metadata['match']

            if hard_article_url is None:
                logging.warning(f'No match found for easy article: {easy_article_url}')
                continue

            logging.info(f'Scraping the hard article: {hard_article_url}')

            hard_metadata, hard_content, hard_html = self._get_hard_article_metadata_and_content(hard_article_url)

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
    MDRCurrentScraper().scrape()

