import os
import pandas as pd
import json
import requests
import logging
from datetime import datetime
import subprocess
import ftfy


class DataHandler:
    """
    Methods:
    - head(dir, n): Returns the first n articles from the specified directory.
    - get_first(dir): Retrieves the first article from the specified directory.
    - get_all(dir): Retrieves all articles from the specified directory.
    - save_article(dir, metadata, content, download_audio=True): Saves an article along with its metadata and optional audio.
    - search_by(dir, metadata_attribute, attribute_value): Searches articles by a metadata attribute.
    - is_already_saved(dir, url): Returns bool if url is already saved as article
    """

    def __init__(self, source):
        """
        source (str): The data source. Should be either "dlf" for deutschlandfunk/nachrichten leicht or "mdr" for MDR.
        """
        # get git root (that is where the data folder should be stored)
        try:
            git_root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], text=True
            ).strip()
        except subprocess.CalledProcessError as e:
            logging.error("This directory is not part of a Git repository.")
            raise e

        if source not in ["dlf", "mdr"]:
            raise ValueError(
                f"Invalid source '{source}'. Valid sources are 'dlf' and 'mdr'."
            )

        self.source = source
        self.root = os.path.join(git_root, "data", source)
        self.helper = DataHandlerHelper(self.root)
        self.helper._init_files_and_dirs(source)

    # -------------------------- READ --------------------------
    def head(self, dir, n):
        """
        Args:
            dir (str): The directory to fetch articles from.
            n (int): The number of articles to retrieve.
        """
        dir_path = self.helper._get_e_or_h_path(dir)
        results = []
        try:
            article_dirs = sorted(os.listdir(dir_path))[:n]
        except:
            return None

        for article_dir in article_dirs:
            article_path = os.path.join(dir_path, article_dir)
            results.append(self.helper._read_article_from_folder(article_path))

        return pd.concat(results)

    def get_first(self, dir):
        """
        Args:
            dir (str): The directory to fetch the first article from.
        """
        return self.head(dir, 1)

    def get_all(self, dir):
        """
        Args:
            dir (str): The directory to retrieve all articles from.
        """
        dir_path = self.helper._get_e_or_h_path(dir)
        n = self.helper._dir_len(dir_path)
        return self.head(dir, n)

    # -------------------------- WRITE --------------------------
    def save_article(self, dir, metadata, content, html, download_audio=True):
        """
        Args:
            dir (str): The directory where the article should be saved.
            metadata (dict): Article metadata including title, date, and URL.
            content (str): The text content of the article.
            download_audio (bool): Whether to download audio files associated with the article.
            html (str): The raw html content of the article
        """
        # some matchers give back non utf8 chars which causes problems especially with pandas
        path = self.helper._get_e_or_h_path(dir)
        dir_path = self.helper._create_filepath(
            path, metadata["date"], metadata["title"]
        )

        if dir_path is None:
            logging.info(f'Already saved {metadata["url"]} ')
            return

        logging.info(f'Saving {metadata["url"]}')
        self.helper._update_lookup_file(dir, dir_path, metadata["url"])
        self.helper._save_content(content, dir_path)
        self.helper._save_metadata(metadata, dir_path)
        self.helper._save_html(html, dir_path)

        if download_audio:
            self.helper._save_audio(metadata, dir_path)

    # -------------------------- SEARCH --------------------------
    def search_by(self, dir, metadata_attribute, attribute_value):
        """
        Args:
            dir (str): The directory to search within.
            metadata_attribute (str): The metadata field to search by.
            attribute_value (str): The value to match in the metadata field.
        """
        path = self.helper._get_e_or_h_path(dir)
        if metadata_attribute == "url":
            return self.helper._search_url_in_lookup(dir, attribute_value)
        else:
            path = self.helper._get_e_or_h_path(dir)
            for art in os.listdir(path):
                art_path = os.path.join(path, art)
                if os.path.isdir(art_path):
                    metadata_path = os.path.join(art_path, "metadata.json")
                    try:
                        with open(
                            metadata_path, "r", encoding="utf-8", errors="replace"
                        ) as f:
                            metadata = json.load(f)
                            if metadata.get(metadata_attribute) == attribute_value:
                                return art_path
                    except FileNotFoundError:
                        logging.error(f"No metadata.json found in {art_path}")
                    except json.JSONDecodeError:
                        logging.error(f"Invalid JSON in {metadata_path}")
            return None

    def is_already_saved(self, dir, url):
        """
        Args:
            dir (str): The directory to search within.
            url (str): url of the article
        """
        if self.search_by(dir, "url", url) == None:
            return False
        else:
            return True


class DataHandlerHelper(DataHandler):
    """
    for better readbility of the DataHandler class this class contains all functions
    that are not functions for the Datahandler interface but needed intern in the DataHandler
    """

    def __init__(self, root):
        self.root = root
        self.lookup_easy_path = None
        self.lookup_hard_path = None

    def _init_files_and_dirs(self, source):
        # make shure data and data/easy and data/hard exist
        os.makedirs(self.root, exist_ok=True)
        os.makedirs(os.path.join(self.root, "easy"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "hard"), exist_ok=True)

        # Check and initialize the CSV file
        csv_path = os.path.join(self.root, "matches_" + source + ".csv")
        if not os.path.isfile(csv_path):
            df = pd.DataFrame(columns=["easy", "hard"])
            df.to_csv(csv_path, index=False)
    
        # init lookup
        self.lookup_easy_path = os.path.join(
            self.root, "easy", "lookup_" + source + "_easy.csv"
        )
        if not os.path.isfile(self.lookup_easy_path):
            df = pd.DataFrame(columns=["path", "url"])
            df.to_csv(self.lookup_easy_path, index=False)

        self.lookup_hard_path = os.path.join(
            self.root, "hard", "lookup_" + source + "_hard.csv"
        )
        if not os.path.isfile(self.lookup_hard_path):
            df = pd.DataFrame(columns=["path", "url"])
            df.to_csv(self.lookup_hard_path, index=False)

    def _get_e_or_h_path(self, dir):
        if dir not in ("e", "h", "easy", "hard"):
            raise Exception(dir + " is not a valid directory")

        return os.path.join(
            self.root, "easy" if dir == "e" or dir == "easy" else "hard"
        )

    def _read_article_from_folder(self, article_path):
        if not os.path.exists(article_path):
            raise FileNotFoundError(f"{article_path} does not exist")

        metadata_path = os.path.join(article_path, "metadata.json")
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)
            metadata_df = pd.json_normalize(metadata, sep="_")

        content_path = os.path.join(article_path, "content.txt")
        with open(content_path, "r", encoding="utf-8") as content_file:
            text_content = content_file.read()

        metadata_df["text"] = text_content
        return metadata_df

    def _dir_len(self, dir):
        return len(
            [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
        )

    def _create_filepath(self, directory, date, title):
        if date is None:
            date = datetime.today().strftime("%Y-%m-%d")
        if title is None:
            title = "Title Missing"
        title = self._clean_file_path(title)
        filepath = os.path.join(directory, date + "-" + title.replace(" ", "_"))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            return filepath
        else:
            return None

    def _save_content(self, content, filepath):
        filepath = os.path.join(filepath, "content.txt")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

    def _save_audio(self, metadata, filepath):
        if "audio" in metadata and metadata["audio"]:
            filepath = os.path.join(filepath, "audio.mp3")
            audio = metadata["audio"]
            mp3 = requests.get(audio["download_url"])
            with open(filepath, "wb") as file:
                file.write(mp3.content)

    def _save_metadata(self, metadata, filepath):
        filepath = os.path.join(filepath, "metadata.json")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(json.dumps(metadata, indent=4))

    def _clean_file_path(self, input_string):
        # chars that will be replaced
        replace_mapping = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "Ä": "Ae",
            "Ö": "Oe",
            "Ü": "Ue",
            "ß": "ss",
        }
        # chars that will be removed
        invalid_chars = set('<>:"/\\|?*.,!§$%&/(){[]}\0\n\t\r\u2013')
        cleaned_string = "".join(
            # if c is not it dict use c else use the value of the dict
            replace_mapping.get(c, c)
            for c in input_string
            if c not in invalid_chars
        )
        return cleaned_string

    def _update_lookup_file(self, dir, article_path_string, url):
        if dir in ["e", "easy"]:
            table = self.lookup_easy_path
        elif dir in ["h", "hard"]:
            table = self.lookup_hard_path
        with open(table, "a") as f:
            f.write(f"{article_path_string}, {url}\n")

    def _search_url_in_lookup(self, dir, url):
        if dir in ["e", "easy"]:
            table = self.lookup_easy_path
        elif dir in ["h", "hard"]:
            table = self.lookup_hard_path
        df = pd.read_csv(table)
        res = df.loc[df["url"].str.contains(url), "path"]
        if not res.empty:
            return res.iloc[0]
        else:
            return None

    def _save_html(self, html, filepath):
        filepath = os.path.join(filepath, "raw.html")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html)
            
