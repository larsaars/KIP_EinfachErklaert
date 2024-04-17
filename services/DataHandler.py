import os
import pandas as pd
import numpy as np
from datetime import datetime
import json
import requests
import logging


class DataHandler:
    def __init__(self, source):
        """
        Initializes a DataHandler object.

        Args:
            source (str): The data source. Should be either "dlf" for deutschlandfunk/nachrichten leicht or "mdr" for MDR.
                Raises:
                    Exception: If an invalid source is provided.
        """
        
        if source == "dlf":
            self.root = os.path.join(".", "data", "deutschlandfunk")
        elif source == "mdr":
            self.root = os.path.join(".", "data", "mdr")
        else:
            raise Exception(
                f"Invalid source '{source}' provided. Valid sources are 'dlf' and 'mdr'."
            )
        
        # lookup file we might need later
        lookup_file_name = "lookup.csv"
        self.lookup_easy = os.path.join(self.root, "easy", lookup_file_name)
        self.lookup_hard = os.path.join(self.root, "hard", lookup_file_name)
        
    # ----- READING ----
    def head(self, n, dir):
        """
        Args:
            dir = "e" or "h" or "easy" or "hard
        Returns:
            Pandas Data Frame:(alphabetically) first n articles from easy or hard OR
            as many as avaliable if n < articles stored
        """
        # Error Handling
        if dir not in ("e", "h", "easy", "hard"):
            raise Exception(dir + " is not a valid directory")

        dir_path = os.path.join(
            self.root, "easy" if dir == "e" or dir == "easy" else "hard"
        )
        articles_df = pd.DataFrame(
            index=np.arange(n), columns=["url", "title", "date", "text"]
        )

        article_dirs = sorted(os.listdir(dir_path))[:n]
        i = 0

        for article_dir in article_dirs:
            article_path = os.path.join(dir_path, article_dir)
            articles_df.iloc[i] = self.__read_article_from_folder(article_path)
            i += 1

        # Remove any unused rows
        articles_df.dropna(how="all", inplace=True)

        return articles_df

    def get_first(self, dir):
        """
        Args:
            dir = "e" or "h" or "easy" or "hard
        Returns:
            Pandas Data Frame:(alphabetically) first article from easy or hard
        """
        return self.head(1, dir)

    def get_all(self, dir):
        """
        Args:
            dir = "e" or "h" or "easy" or "hard
        Returns:
            Pandas Data Frame: all articles from easy or hard
        """
        dir_path = os.path.join(
            self.root, "easy" if dir == "e" or dir == "easy" else "hard"
        )
        n = self.__dir_len(dir_path)
        return self.head(n, dir)

    def __read_article_from_folder(self, article_path):
        """
        Reads metadata and text content from an article folder and returns it as a pandas DataFrame.
        Keeps only specified columns from the metadata.

        Args:
            article_path: Path to the folder containing the article's files.

        Returns:
            pandas.DataFrame: A DataFrame with a single row containing specified article metadata and text.
        """
        if not os.path.exists(article_path):
            raise FileNotFoundError(f"{article_path} does not exist")

        columns_to_keep = ["url", "title", "date"]

        metadata_path = os.path.join(article_path, "metadata.json")
        with open(metadata_path, "r", encoding="utf-8", errors="replace") as file:
            metadata = pd.read_json(file, typ="series")[columns_to_keep]

        content_path = os.path.join(article_path, "content.txt")
        if os.path.exists(content_path):
            with open(
                content_path, "r", encoding="utf-8", errors="replace"
            ) as content_file:
                text_content = content_file.read()
        else:
            text_content = np.nan

        metadata["text"] = text_content

        return pd.DataFrame([metadata])

    def __dir_len(self, dir):
        return len(
            [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
        )

    # ----- WRITE -----

    def save_article(self, dir, metadata, content, download_audio=True):
        """
        Saves an article to the specified directory.

        Args:
            dir (str): The directory to save the article in. Should be "e" or "easy" for easy articles, or "h" or "hard" for hard articles.
            metadata (dict): Metadata of the article including "url", "title", "date", and optionally "audio" containing audio download_url.
            content (str): The content of the article.
            download_audio (bool, optional): Whether to download and save audio associated with the article. Defaults to True.
        Raises:
            Exception: If an invalid directory is provided.
        """
        if dir not in ("e", "h", "easy", "hard"):
            raise Exception(dir + " is not a valid directory")

        dir_path = os.path.join(
            self.root, "easy" if dir == "e" or dir == "easy" else "hard"
        )
        
        dir_path = self.__create_filepath(dir_path, metadata["date"], metadata["title"])
        
        # check if article was already scraped by if folder existed
        if dir_path is None:
            logging.info(f'Already scraped {metadata["url"]} ')
            return
        
        logging.info(f'Scraping {metadata["url"]}')
        
        # if it was not scraped 
        self.__update_lookup_file(dir, str(dir_path), metadata["url"])
        self.__save_content(content, dir_path)
        self.__save_metadata(metadata, dir_path)
        if download_audio:
            self.__save_audio(metadata, dir_path)

    def __create_filepath(self, directory, date, title):
        title = self.__clean_file_path(title)
        date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        filepath = os.path.join(directory, date + "-" + title.replace(" ", "_"))
        # init directory
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            return filepath
        else: 
            return None

    def __save_content(self, content, filepath):
        filepath = os.path.join(filepath, "content.txt")
        with open(filepath, "w", encoding="utf-8", errors="replace") as file:
            file.write(content)

    def __save_audio(self, metadata, filepath):
        filepath = os.path.join(filepath, "audio.mp3")
        audio = metadata["audio"]
        if audio:
            mp3 = requests.get(audio["download_url"])
            with open(filepath, "wb") as file:
                file.write(mp3.content)

    def __save_metadata(self, metadata, filepath):
        filepath = os.path.join(filepath, "metadata.json")
        with open(filepath, "w", encoding="utf-8", errors="replace") as file:
            file.write(json.dumps(metadata, indent=4))

    def __clean_file_path(self, input_string):
        """
        Removes all characters not allowed in Windows or Linux file paths, some non ascii chars and german umlauts from input_string
        """
        umlaut_mapping = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "Ä": "Ae",
            "Ö": "Oe",
            "Ü": "Ue",
        }

        invalid_chars = set('<>:"/\\|?*.,!§$%&/(){[]}') | {"\0"}
        cleaned_string = "".join(
            umlaut_mapping.get(c, c) for c in input_string if c not in invalid_chars
        )
        return cleaned_string
        
    def __update_lookup_file(self, dir, path, url):
        
        if dir in ("e", "easy"):
            file = self.lookup_easy
        else:
            file = self.lookup_hard
            
        with open(file,'a') as f:
            f.write(f'{path}, {url}\n')
            
            

        
