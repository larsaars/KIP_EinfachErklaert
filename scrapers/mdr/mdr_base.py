#!/usr/bin/env python3

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

"""Base class of the MDR current and historic scraper, contains functions 
for scraping metadata and content for both hard and 
easy articles"""
class MDRBaseScraper(BaseScraper):
    def __init__(self):
        """init MDRBaseScraper class
        Args:
            driver: selenium webdriver"""

        super().__init__('mdr')  # init BaseScraper with source name

        self._driver = self._init_selenium()  # init selenium webdriver

        # dict to map month names to numbers for date formatting
        self.month_mapping = {
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


    def _init_selenium(self):
        """init selenium webdriver
            
        Returns:
            webdriver: selenium webdriver
        """

        # configure selenium (is needed for button clicking)
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument('--ignore-certificate-errors')  # ignore ssl errors
        driver_options.add_argument('--incognito')  # private mode
        driver_options.add_argument('--headless')  # no sandbox
        return webdriver.Chrome(options=driver_options)  # create the driver
    

    def _try_audio_extraction(self, soup, metadata):
        """try to extract audio from the article

        Args:
            soup: BeautifulSoup object of the article
            metadata: metadata dict of the article
        """

        audio = base_audio_dict()  # audio dict to be returned

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


    def _get_easy_article_metadata_and_content(self, url):
        """
        Get the metadata, content and html source of an easy MDR article.

        Args:
            url (str): url of the article

        Returns:
            dict: metadata of the article
        """

        metadata = base_metadata_dict()  # metadata dict to be returned
        
        self._driver.get(url)  # open the article in the browser (for js execution)

        html = self._driver.page_source  # get the html of the page

        # get soup of the article
        soup = BeautifulSoup(html, 'html.parser')


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

        try:
            metadata['title'] = soup.find('span', class_='headline').text  # title
        except Exception:
            logging.error('Error while parsing title')

        try:
            metadata['kicker'] = soup.find('span', class_='dachzeile').text  # kicker
        except Exception:
            logging.error('Error while parsing kicker')

        # try to get the date and format it (MM-DD-YYYY)
        try:
            date_text = soup.find('p', class_='webtime').text  # multiline date text
            date_text = date_text.split('\n')[1]  # get the second line (which contains the date)
            day, month, year = date_text.split()  # split the date into day, month, year
            month = self.month_mapping[month]  # map the month name to a number
            day, year = day[:-1], year[:-1]  # remove the trailing comma from the day and year
            metadata['date'] = f'{year}-{month}-{day}'  # format the date
        except Exception:
            logging.error('Error while parsing date')

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            logging.error('Error while parsing image')


        # try audio extraction
        self._try_audio_extraction(soup, metadata)

        # try to get the hard article url
        try:
            match_url = 'https://mdr.de' + soup.find_all('a', class_='linkAll')[1]['href']  # this is typically the match url

            # sometimes, there is no match url in the article
            # then the match url contains a 'nachrichten-leicht' substring
            # or a 'mdr.de/video/mdr-videos' substring

            error = False

            if 'nachrichten-leicht' in match_url:
                logging.error('Matching error: Article has no hard match (linking to a easy news article (feed))')
                error = True

            if 'mdr.de/video/mdr-videos' in match_url:
                logging.error('Matching error: Video article: Skipping')
                error = True

            if 'nachrichtenfeed' in match_url:
                logging.error('Matching error: Article has no hard match (linking to a news feed)')
                error = True


            if error:
                metadata['match'] = None
            else:
                metadata['match'] = match_url  # set the match url if no error occured
            
        except Exception:
            logging.error('Error while parsing hard article url')


        return metadata, content, html


        
    def _get_hard_article_metadata_and_content(self, url):
        """
        Get the metadata, content and html of a hard language MDR article.

        Args:
            url (str): url of the article

        Returns:
            dict: metadata of the article
        """

        metadata = base_metadata_dict()  # metadata dict to be returned
        
        self._driver.get(url)  # open the article in the browser (for js execution)

        html = self._driver.page_source  # get the html of the page

        # get soup of the article
        soup = BeautifulSoup(html, 'html.parser')


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
            month = self.month_mapping[month]  # map the month name to a number
            day, year = day[:-1], year[:-1]  # remove the trailing comma from the day and year
            metadata['date'] = f'{year}-{month}-{day}'  # format the date
        except Exception:
            logging.error('Error while parsing date')

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            logging.error('Error while parsing image')


        # try to extract audio
        self._try_audio_extraction(soup, metadata)


        return metadata, content, html

    def __del__(self):
        # destroy webdriver
        if hasattr(self, '_driver'):
            self._driver.quit()
    
