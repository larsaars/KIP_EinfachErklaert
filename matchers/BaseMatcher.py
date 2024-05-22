import os
import sys
# import root dir to easily import data handler
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)
from services.DataHandler import DataHandler

class BaseMatcher:

    def __init__(self, source):
        """
        source (str): The data source. Should be either "dlf" for deutschlandfunk/nachrichten leicht or "mdr" for MDR.
        """
        if source == "dlf":
            self.root = os.path.join(".", "data", "deutschlandfunk")
            self.file = os.path.join(self.root, "matches_deutschlandfunk.csv")
        elif source == "mdr":
            self.root = os.path.join(".", "data", "mdr")
            self.file = os.path.join(self.root, "matches_mdr.csv")
        else:
            raise Exception(
                f"Invalid source '{source}' provided. Valid sources are 'dlf' and 'mdr'."
            )
            
        self.data_handler = DataHandler(source)
        
    def write_match(self, easy, hard):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"{easy}, {hard}\n")