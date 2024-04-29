#!/usr/bin/env python3

"""
Scrapes the current articles from WDR (easy & hard language) and saves them to the database.
"""

import sys

# add parent dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append('../..')

from time import sleep
import json
import xml.etree.ElementTree as ET
import requests

from scrapers.base_scraper import BaseScraper, base_metadata_dict
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

        # try to get the date and format it in a way the datahandler can handle (DD.MM.YYYY)
        try:
            date_text = soup.find('p', class_='webtime').text  # multiline date text
            date_text = date_text.split('\n')[1]  # get the second line (which contains the date)
            day, month, year = date_text.split()  # split the date into day, month, year
            month = month_mapping[month]  # map the month name to a number
            year = year[:-1]  # remove the trailing comma from the year
            metadata['date'] = f'{day}{month}.{year}'  # format the date (day already contains the trailing '.')
        except Exception:
            pass

        try:
            img = soup.find('img')
            metadata['image_url'] = img['src']  # image url
            metadata['image_description'] = img['alt']  # image description
        except Exception:
            pass

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
            metadata['audio']['download_url'] = xml_parsed.findall('.//assets/asset')[2].find('progressiveDownloadUrl').text  # get the audio url (index 2 is mp3 format, index 0 would be mp4)
        except Exception:
            pass

        # try to get the hard article url
        try:
            metadata['match'] = 'https://mdr.de' + soup.find_all('a', class_='linkAll')[1]['href']
        except Exception:
            pass


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
            self.data_handler.save_article('easy', metadata, content, download_audio=True)
            # append to the list
            easy_and_hard_articles.append({
                'easy': metadata['url'],
                'hard': metadata['match']
            })

        return easy_and_hard_articles



if __name__ == '__main__':
    # configure selenium (is needed for button clicking)
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--ignore-certificate-errors')  # ignore ssl errors
    driver_options.add_argument('--incognito')  # private mode
    # options.add_argument('--headless')  # no browser window
    driver = webdriver.Chrome(options=driver_options)  # create the driver


    # start scraping the easy articles, from which we can extract the hard article urls
    easy_and_hard_articles = MDREasyScraper(driver=driver).scrape()
    # use this list of hard article urls to scrape the hard articles
    # TODO: MDRHardScraper(easy_and_hard_articles).scrape()

    # close the webdriver
    driver.quit()
