import requests
from bs4 import BeautifulSoup
import logging
import sys
import os

# import root dir to easily import data handler
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)
from services.DataHandler import DataHandler


hard_feed_url = "https://www.deutschlandfunk.de/nachrichten-100.html"
easy_feed_url = "https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems=0&drsearch:itemsPerLoad=30&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1"


def get_soup(url):
    try:
        response = requests.get(url)
    except Exception:
        print("Failed fetching response. URL:", url)
        return
    return BeautifulSoup(response.text, "html.parser")


def get_articles_from_feed(feed):
    article_refs = feed.find_all("article")
    articles = []
    for article in article_refs:
        try:
            url = article.find("a")["href"]
            headline = article.find("a")["title"]
        except Exception:
            continue
        try:
            description = article.find("p", class_="article-info-content").text.strip()
        except Exception:
            description = None
        try:
            image_url = article.find("img")["src"]
        except Exception:
            image_url = None
        data = {
            "url": url,
            "headline": headline,
            "description": description,
            "image_url": image_url,
        }
        articles.append(data)
    return articles


# ---- ARTICLE FUNCTIONS ----


def get_article_from_url(url):
    article_html = get_soup(url)
    return article_html.find("article", class_="b-article")


def get_article_content(article):
    content = []
    for child in article.find(class_="b-article-details").children:
        if child.name == "h2":
            content.append(child.text)
        if child.name == "div":
            content.append(child.text)
    return "\n".join(content)


def find_string(article, *args, **kwargs):
    try:
        content = article.find(*args, **kwargs).string
    except Exception:
        content = None
    return content


def get_deutschlandfunk_metadata(article, article_url):
    title = find_string(article, class_="headline-title")
    kicker = find_string(article, class_="headline-kicker")
    date = find_string(article, class_="article-header-author")
    description = find_string(article, class_="article-header-description")
    image_des = find_string(article, "figcaption")
    try:
        image_url = article.find("img")["src"]
        image_des = article.find("figcaption").string
    except Exception:
        image_url = None
        image_des = None
    metadata = {
        "title": title,
        "description": description,
        "kicker": kicker,
        "date": date,
        "url": article_url,
        "image_url": image_url,
        "image_description": image_des,
        "audio": None,
    }
    return metadata


def get_nachrichtenleicht_audio(article):
    try:
        audio = article.find(class_="js-audio")
    except Exception:
        return None
    if not audio:
        return None
    return {
        "audio_url": audio["href"],
        "download_url": audio["data-audio-download-src"],
        "duration": audio["data-audioduration"],
    }


def get_nachrichtenleicht_metadata(article, article_url):
    title = find_string(article, class_="article-header-title")
    kicker = find_string(article, class_="headline-kicker")
    date = find_string(article, class_="article-header-author")
    description = find_string(article, class_="article-header-description")
    image_des = find_string(article, "figcaption")
    audio_data = get_nachrichtenleicht_audio(article)
    try:
        image_url = article.find("img")["src"]
        image_des = article.find("figcaption").string
    except Exception:
        image_url = None
        image_des = None
    metadata = {
        "title": title,
        "description": description,
        "kicker": kicker,
        "date": date,
        "url": article_url,
        "audio": audio_data,
        "image_url": image_url,
        "image_description": image_des,
    }
    return metadata


def get_deutschlandfunk_article(url):
    article = get_article_from_url(url)
    content = get_article_content(article)
    metadata = get_deutschlandfunk_metadata(article, url)
    article_data = {"metadata": metadata, "content": content}
    return article_data


def get_nachrichtenleicht_article(url):
    article = get_article_from_url(url)
    content = get_article_content(article)
    metadata = get_nachrichtenleicht_metadata(article, url)
    article_data = {"metadata": metadata, "content": content}
    return article_data


# ---- MAIN ----

# run with python3 -m scraper.scraper_with_DataHandler from KIP_EinfachErklaert
def main():
    # scrape articles
    easy_articles = get_articles_from_feed(get_soup(easy_feed_url))
    hard_articles = get_articles_from_feed(get_soup(hard_feed_url))
    
    dh = DataHandler("dlf")
    
    # safe easy (nachrichtenleicht)
    for e_article in easy_articles:
        
        article_data_dict = get_nachrichtenleicht_article(e_article["url"])
        metadata = article_data_dict["metadata"]
        content = article_data_dict["content"] # content = main text
        # pass metadata as dict and content as string to safe_article
        # for now passing in the the right data types is the scapers job
        dh.save_article("easy", metadata, content, download_audio=False)
        
    # safe hard (deutschlandfunk)
    for h_article in hard_articles:
        
        article_data_dict = get_deutschlandfunk_article(h_article["url"])
        metadata = article_data_dict["metadata"]
        content = article_data_dict["content"] 
        dh.save_article("hard", metadata, content, download_audio=False)
        
    print("SCRAPING AND SAVING FINISHED!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()