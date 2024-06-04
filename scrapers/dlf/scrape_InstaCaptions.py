#TODO: make captions saveable

import instaloader
import logging
import sys
import subprocess
import requests
import re

sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

from scrapers.base.base_scraper import BaseScraper
from PIL import Image
from io import BytesIO
import pytesseract


def clean_text(text):
    # Encode to UTF-8 and decode back to a string
    text = text.encode("utf-8", "ignore").decode("utf-8")

    # Remove newline characters
    text = text.replace("\n", " ")

    # Remove non-alphanumeric characters
    text = text.replace("-", "")
    text = re.sub(r'\W+', ' ', text)

    # Limit to the first 10 words
    words = text.split()
    text = ' '.join(words[:12])

    # Delete Words in Caps and the trailing spaces of the words
    text = re.sub(r'\b[A-Z]+\b', '', text)

    return text

def text_from_image(url):
    image = Image.open(BytesIO(requests.get(url).content))
    text = pytesseract.image_to_string(image, lang='deu')
    return clean_text(text)


def base_metadata_dict(post: instaloader.Post) -> dict:
    metadata = {"title": text_from_image(post.url),
                "description": post.caption,
                "url": post.url,
                "date": post.date_utc.strftime("%Y-%m-%d"),
                "kicker": post.caption_hashtags}
    return metadata


class InstaScraper(BaseScraper):
    def __init__(self):
        super().__init__("dlf")
        self.L = instaloader.Instaloader()
        self.username = "nachrichtenleicht"
        self.profile = instaloader.Profile.from_username(self.L.context, self.username)

    def scrape(self):
        for post in self.profile.get_posts():
            if not self.data_handler.is_already_saved("easy", post.url):
                if post.caption[:5] == "Unser":
                    continue
                metadata = base_metadata_dict(post)
                content = post.caption
                self.data_handler.save_article("easy", metadata, content, post.url, download_audio=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    InstaScraper().scrape()
