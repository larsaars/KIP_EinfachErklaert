import os
import pandas as pd
import numpy as np

"""
einfacherklaert/
├─ deutschlandfunk/
│  ├─ easy/
│  │  ├─ article-abcdef/
│  │  │  ├─ content.txt
│  │  │  ├─ audio.mp3
│  │  │  ├─ metadata.json
│  │  ├─ article-ghasdf/
│  │  
│  ├─ hard/
│  │  ├─ article-sdfdgd/
│  │  │  ├─ content.txt
│  │  │  ├─ audio.mp3
│  │  │  ├─ metadata.json
├─ matchings.txt
"""


class DataHandler:
    def __init__(self, source):
        # deutschlandfunk/ nachrichten leicht
        if source == "df":
            # TODO : Adapt this to the directory from which this script is executed
            self.root = os.path.join("..", "data", "deutschlandfunk")

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
        n = self.__len(dir_path)
        return self.head(n, dir)

    def write_article(self, url, title, text, date):
        pass

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
            with open(content_path, "r") as file:
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

    def __len(self, dir):
        return len(
            [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
        )

