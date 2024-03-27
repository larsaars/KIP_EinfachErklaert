"""
import requests
from bs4 import BeautifulSoup

h_url = 'https://www.deutschlandfunk.de/nachrichten-100.html'
e_url = 'https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems=0&drsearch:itemsPerLoad=30&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1'

response = requests.get(h_url)

soup = BeautifulSoup(response.text, 'html.parser')

html_articles = soup.find_all('article')

articles_h = []

for html_article in html_articles:
    try:
        url = html_article.find('a')['href']
        headline = html_article.find('a')['title']
    except Exception:
        continue
    try:
        description = html_article.find('p', class_='article-info-content').text.strip()
    except Exception:
        description = None
    try:
        image_url = html_article.find('img')['src']
    except Exception:
        image_url = None

    data = {'url': url, 'headline': headline, 'description': description, 'image_url': image_url}

    articles_h.append(data)

response = requests.get(e_url)

soup = BeautifulSoup(response.text, 'html.parser')

html_articles = soup.find_all('article')

articles_e = []

for html_article in html_articles:
    try:
        audio_url = html_article.find('button')['data-audioreference']
    except Exception:
        audio_url = None  # oder einen Standardwert zuweisen

    data = {'url': html_article.find('a')['href'],
            'headline': html_article.find('a')['title'],
            'description': html_article.find('p', class_='teaser-wide-description').text.strip(),
            'image_url': html_article.find('img')['src'],
            'audio_url': audio_url}

    articles_e.append(data)

print(articles_e)
print(len(articles_e))
print(articles_h)
print(len(articles_h))
"""

import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

csv_path_h = 'articles_h.csv'
csv_path_e = 'articles_e.csv'

# csv check
if os.path.exists(csv_path_h):
    df_h = pd.read_csv(csv_path_h)
else:
    df_h = pd.DataFrame(columns=['url', 'headline', 'description', 'image_url'])

if os.path.exists(csv_path_e):
    df_e = pd.read_csv(csv_path_e)
else:
    df_e = pd.DataFrame(columns=['url', 'headline', 'description', 'image_url', 'audio_url'])

h_url = 'https://www.deutschlandfunk.de/nachrichten-100.html'
e_url = 'https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems=0&drsearch:itemsPerLoad=30&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1'

response = requests.get(h_url)
soup = BeautifulSoup(response.text, 'html.parser')
html_articles = soup.find_all('article')
articles_h = []
for html_article in html_articles:
    try:
        url = html_article.find('a')['href']
        headline = html_article.find('a')['title']
    except Exception:
        continue
    try:
        description = html_article.find('p', class_='article-info-content').text.strip()
    except Exception:
        description = None
    try:
        image_url = html_article.find('img')['src']
    except Exception:
        image_url = None
    data = {'url': url, 'headline': headline, 'description': description, 'image_url': image_url}
    articles_h.append(data)

response = requests.get(e_url)
soup = BeautifulSoup(response.text, 'html.parser')
html_articles = soup.find_all('article')
articles_e = []
for html_article in html_articles:
    try:
        audio_url = html_article.find('button')['data-audioreference']
    except Exception:
        audio_url = None
    data = {'url': html_article.find('a')['href'],
            'headline': html_article.find('a')['title'],
            'description': html_article.find('p', class_='teaser-wide-description').text.strip(),
            'image_url': html_article.find('img')['src'],
            'audio_url': audio_url}
    articles_e.append(data)

new_df_h = pd.DataFrame(articles_h)
new_df_e = pd.DataFrame(articles_e)

df_h = pd.concat([df_h, new_df_h]).drop_duplicates().reset_index(drop=True)
df_e = pd.concat([df_e, new_df_e]).drop_duplicates().reset_index(drop=True)

df_h.to_csv(csv_path_h, index=False)
df_e.to_csv(csv_path_e, index=False)