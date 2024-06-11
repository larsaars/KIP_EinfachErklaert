import os
import sys
import subprocess
import logging
# import root dir to easily import data handler
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)
from datahandler.DataHandler import DataHandler
from datetime import datetime

class BaseMatcher:

    def __init__(self, source):
        """
        source (str): The data source. Should be either "dlf" for deutschlandfunk/nachrichten leicht or "mdr" for MDR.
        """
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
        self.file = os.path.join(self.root, f"matches_{source}.csv")     
        self.data_handler = DataHandler(source)
        
    def write_match(self, easy, hard):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}, {easy}, {hard}\n")