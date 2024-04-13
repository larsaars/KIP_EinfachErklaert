#!/usr/bin/env python3

"""
I created this script as an example how we could scrape historic deutschlandfunk.de news articles.
If used, this has yet to be merged with scraper.py and its functions.
(Everything has to be put together with the database functions as well as the other scrapers bla bla).
TODO

I use selenium since BeautifulSoup is only a parser, but I have to scrape contents that load after interaction with the website.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# TODO generalize (no xpath!)
# TODO for different dates
# TODO get urls of loaded items

# Initialize a Selenium webdriver
driver = webdriver.Chrome()

# Load the webpage
driver.get('https://www.deutschlandfunk.de/programm?drsearch:date=2024-04-10')

# Click the button that loads the additional content
button = driver.find_element('xpath', '/html/body/div[1]/main/section[3]/ul/li[48]/section/div/div[4]/div/div/div/button/span')
button.click()

# Wait for the content to load
timeout = 10  # Adjust the timeout as needed
try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/section[3]/ul/li[48]/section/div/div[4]/div/div/div/div/div/article[1]'))
    )
except TimeoutException:
    print("Timed out waiting for content to load")
    driver.quit()
    exit()

# Once the content is loaded, get the page source
page_source = driver.page_source

# Quit the driver
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Now use BeautifulSoup to extract the desired information from the loaded contenturce
urls = []  # list that will contain the news urls

# get the first url (is in a different div)
print(soup.find(xpath='/html/body/div[1]/main/section[3]/ul/li[48]/section/div/div[4]/div/div/div/div/article/div[2]/a'))

