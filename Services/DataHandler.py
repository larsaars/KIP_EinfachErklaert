import os
import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataHandler:
    def __init__(self, source):
        # deutschlandfunk/ nachrichten leicht
        if source == "df":
            # TODO : Adapt this to the directory from which this script is executed
            self.root = os.path.join("..", "data", "deutschlandfunk")

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
            index=np.arange(n), columns=["url", "title", "text", "date"]
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
        Args:
            article_path: os.path to folder which stores the article
        Returns:
            Pandas Data Frame: Article specified by dir path and article dir
        """
        # read metadata
        content_path = os.path.join(article_path, "metadata.json")
        if os.path.exists(article_path):
            with open(content_path, "r", encoding='utf-8', errors='replace') as file:
                temp = pd.read_json(file).iloc[0].to_dict()

                # read text only if metadata avaliable
                content_path = os.path.join(article_path, "content.txt")
                if os.path.exists(content_path):
                    with open(content_path, "r") as content_file:
                        temp["text"] = content_file.read()
                else:
                    temp["text"] = np.nan

                return temp
        else:
            raise Exception(article_path + " is not existing")

    def __dir_len(self, dir):
        return len(
            [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
        )

    # ----- WRITE -----

    def save_article(self, dir, metadata, content, audio=None):
        # Error Handling
        if dir not in ("e", "h", "easy", "hard"):
            raise Exception(dir + " is not a valid directory")

        dir_path = os.path.join(
            self.root, "easy" if dir == "e" or dir == "easy" else "hard"
        )

        self.__create_filepath(dir_path, metadata["date"], metadata["title"])
        self.__save_content(content, dir_path)
        self.__save_metadata(metadata, dir_path)
        if audio:
            self.__save_audio(metadata, dir_path)

    def __create_filepath(self, directory, date, title):
        title = self.__clean_file_path(title)
        date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        filepath = os.path.join(directory, date + "-" + title.replace(" ", "_"))
        # init directory
        if not os.path.exists(filepath):
            os.makedirs(filepath)

    def __save_content(self, content, filepath):
        filepath = os.path.join(filepath, "content.txt")
        with open(filepath, "w") as file:
            file.write(content)

    def __save_audio(self, audio, filepath):
        filepath = os.path.join(filepath, "audio.mp3")
        with open(filepath, "wb") as file:
            file.write(audio.content)

    def __save_metadata(self, metadata, filepath):
        filepath = os.path.join(filepath, "metadata.json")
        with open(filepath, "w") as file:
            file.write(json.dumps(metadata, indent=4))
            
    def __clean_file_path(self, input_string):
        """
        Removes all characters not allowed in Windows or Linux file paths from the input string.
        Linux all except '/' and null character.
        Windows all except  '<', '>', ':', '"', '/', '\\', '|', '?', '*', and invalid Unicode characters.
        """
  
        invalid_chars = set('<>:"/\\|?*') | {'\0'}
        cleaned_string = ''.join(c for c in input_string if c not in invalid_chars)
        return cleaned_string
