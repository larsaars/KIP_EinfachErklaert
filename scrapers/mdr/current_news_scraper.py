#!/usr/bin/env python3

"""
Scrapes the current articles from WDR (easy & hard language) and saves them to the database.
"""

import sys
import os
import logging
import subprocess

# add git root dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

from time import sleep
import json
import xml.etree.ElementTree as ET
import requests

from scrapers.base.base_scraper import BaseScraper, base_metadata_dict, base_audio_dict
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By


# dict to map month names to numbers for date formatting
month_mapping = {
    'Januar': '01',
    'Februar': '02',
    'März': '03',
    'April': '04',
    'Mai': '05',
    'Juni': '06',
    'Juli': '07',
    'August': '08',
    'September': '09',
    'Oktober': '10',
    'November': '11',
    'Dezember': '12'
}


class MDREasyScraper(BaseScraper):
    def __init__(self, driver=None): # init with feed url and source
        super().__init__('https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html', 'mdr')

        self.driver = driver  # the selenium webdriver
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
        audio = base_audio_dict()  # audio dict to be returned
        
        self.driver.get(url)  # open the article in the browser (for js execution)

        # get soup of the article
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')


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

        # try to get the date and format it (MM-DD-YYYY)
        try:
            date_text = soup.find('p', class_='webtime').text  # multiline date text
            date_text = date_text.split('\n')[1]  # get the second line (which contains the date)
            day, month, year = date_text.split()  # split the date into day, month, year
            month = month_mapping[month]  # map the month name to a number
            day, year = day[:-1], year[:-1]  # remove the trailing comma from the day and year
            metadata['date'] = f'{month}-{day}-{year}'  # format the date
        except Exception:
            logging.error('Error while parsing date')

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            logging.error('Error while parsing image')

        # try audio download
        # this is a little more complicated since the audio is not directly in the article
        # but i found a workaround:
        # when loading the article with js enabled (thats why we use selenium) the audio player is loaded
        # and in a specific div a json object is stored
        # which contains a link to an xml file which contains the audio link
        try:
            json_string = soup.select('div.mediaCon.avInline.avActivePlay[data-ctrl-player]')[0]['data-ctrl-player']  # get the json string
            json_string = json_string.replace('\'', '"')  # replace single quotes with double quotes
            json_obj = json.loads(json_string)  # parse the json string
            xml_url = 'https://mdr.de' + json_obj['playerXml']  # get the xml url
            xml_content = requests.get(xml_url).text  # get the xml content
            xml_parsed = ET.fromstring(xml_content)  # parse the xml
            audio_url = xml_parsed.findall('.//assets/asset')[2].find('progressiveDownloadUrl').text  # get the audio url (index 2 is mp3 format, index 0 would be mp4)
            audio['download_url'] = audio['audio_url'] = audio_url  # set the audio url
            metadata['audio'] = audio  # set the audio metadata
        except Exception:
            logging.error('Error while parsing audio')

        # try to get the hard article url
        try:
            metadata['match'] = 'https://mdr.de' + soup.find_all('a', class_='linkAll')[1]['href']
        except Exception:
            logging.error('Error while parsing hard article url')


        return content, metadata 

    def scrape(self) -> list:
        """
        Scrapes the articles from the feed and saves them to the database.

        Returns:
            list: list of dicts with easy and hard article urls
        """

        logging.info('Starting scraping of easy articles for MDR')

        easy_and_hard_articles = []  # the list tb returned

        for article_url in self._fetch_articles_from_feed():
            logging.info(f'Scraping easy article: {article_url}')

            content, metadata = self._get_metadata_and_content(article_url)
            # save the article to the database
            self.data_handler.save_article('easy', metadata, content, download_audio=True)
            # append to the list
            easy_and_hard_articles.append({
                'easy': metadata['url'],
                'hard': metadata['match']
            })

        return easy_and_hard_articles


class MDRHardScraper(BaseScraper):
    def __init__(self, driver, easy_and_hard_articles: list):
        super().__init__(None, 'mdr')

        self.driver = driver  # the selenium webdriver

        # list of easy and hard article urls (in a dict)
        # since the scraping of the hard article links has already been done by the easy scraper
        # only the metadata and content of the hard articles needs to be scraped
        self.easy_and_hard_articles = easy_and_hard_articles 


    def _get_metadata_and_content(self, url):
        """
        Get the metadata and content of the article.

        Args:
            url (str): url of the article

        Returns:
            dict: metadata of the article
        """

        metadata = base_metadata_dict()  # metadata dict to be returned
        audio = base_audio_dict()  # audio dict to be returned
        
        self.driver.get(url)  # open the article in the browser (for js execution)


        # get soup of the article
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')


        # get content from the article
        content = ''
        # loop through h3 tags and get the text of following paragraph divs
        for h3_tag in soup.find_all('h3', class_='subtitle'):
            content += f'<h3>{h3_tag.text.strip()}</h3>\n'  # add the h3 tag text

            # get the following paragraph divs
            # and add the text to the content
            next_sibling = h3_tag.find_next_sibling() 
            while next_sibling and next_sibling.name == 'div' and 'paragraph' in next_sibling.get('class', []):

                # next_sibling is the paragraph div
                paragraph = next_sibling.find('p')  # get the paragraph tag

                for tag in paragraph.find_all(['a']):
                    del tag['data-ctrl-link']  # all links have this attribute which is not needed

                paragraph_text = ''.join([str(c) for c in paragraph.contents])  # stringify the content of the paragraph

                content += paragraph_text  # add the paragraph to the content

                next_sibling = next_sibling.find_next_sibling()  # continue



        # fill the base metadata dict
        metadata['url'] = url  # source url

        try:
            metadata['title'] = soup.find('h1').find('span', class_='headline').text  # title
        except Exception:
            logging.error('Error while parsing title')

        try:
            metadata['kicker'] = soup.find('h1').find('span', class_='dachzeile').text  # kicker
        except Exception:
            logging.error('Error while parsing kicker')

        try:
            metadata['description'] = soup.find('p', class_='einleitung').text  # description
        except Exception:
            logging.error('Error while parsing description')

        # try to get the date and format it (MM-DD-YYYY)
        try:
            date_text = soup.find('p', class_='webtime').text  # multiline date text
            date_text = date_text.split('\n')[1]  # get the second line (which contains the date)
            day, month, year = date_text.split()  # split the date into day, month, year
            month = month_mapping[month]  # map the month name to a number
            day, year = day[:-1], year[:-1]  # remove the trailing comma from the day and year
            metadata['date'] = f'{month}-{day}-{year}'  # format the date
        except Exception:
            logging.error('Error while parsing date')

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            logging.error('Error while parsing image')

        # try audio download
        # this is a little more complicated since the audio is not directly in the article
        # but i found a workaround:
        # when loading the article with js enabled (thats why we use selenium) the audio player is loaded
        # and in a specific div a json object is stored
        # which contains a link to an xml file which contains the audio link
        try:
            json_string = soup.select('div.mediaCon.avInline.avActivePlay[data-ctrl-player]')[0]['data-ctrl-player']  # get the json string
            json_string = json_string.replace('\'', '"')  # replace single quotes with double quotes
            json_obj = json.loads(json_string)  # parse the json string
            xml_url = 'https://mdr.de' + json_obj['playerXml']  # get the xml url
            xml_content = requests.get(xml_url).text  # get the xml content
            xml_parsed = ET.fromstring(xml_content)  # parse the xml
            audio_url = xml_parsed.findall('.//assets/asset')[2].find('progressiveDownloadUrl').text  # get the audio url (index 2 is mp3 format, index 0 would be mp4)
            audio['download_url'] = audio['audio_url'] = audio_url  # set the audio url
            metadata['audio'] = audio  # set the audio metadata
        except Exception:
            logging.error('Error while parsing audio')


        return content, metadata 

    def scrape(self) -> list:
        """
        Go through the list of easy and hard article urls and scrape the hard articles.
        """

        logging.info('Starting scraping of hard articles for MDR')

        for article in self.easy_and_hard_articles:
            # get the easy and hard article urls from dict
            easy_url, hard_url = article['easy'], article['hard']  

            logging.info(f'Scraping hard article: {hard_url}')

            if 'nachrichten-leicht' in hard_url:
                logging.error('Matching error: Easy article url passed to hard scraper')
                continue
            
            if 'mdr.de/video/mdr-videos' in hard_url:
                logging.error('Matching error: Video article: Skipping')
                continue

            # get the metadata and content of the hard article
            content, metadata = self._get_metadata_and_content(hard_url)  
            # set the match to the easy article url
            metadata['match'] = easy_url  
            # save the article to the database
            self.data_handler.save_article('hard', metadata, content, download_audio=True)

        return easy_and_hard_articles


if __name__ == '__main__':
    # configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # configure selenium (is needed for button clicking)
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--ignore-certificate-errors')  # ignore ssl errors
    driver_options.add_argument('--incognito')  # private mode
    # options.add_argument('--headless')  # no browser window
    driver = webdriver.Chrome(options=driver_options)  # create the driver


    # start scraping the easy articles, from which we can extract the hard article urls
    easy_and_hard_articles = MDREasyScraper(driver=driver).scrape()
    # use this list of hard article urls to scrape the hard articles
    MDRHardScraper(driver, easy_and_hard_articles).scrape()

    # close the webdriver
    driver.quit()
