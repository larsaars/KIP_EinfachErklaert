import os
import sys
import subprocess
import pandas as pd
import logging

# Add git root dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append(
    subprocess.check_output("git rev-parse --show-toplevel".split())
    .decode("utf-8")
    .strip()
)

from matchers.BaseMatcher import BaseMatcher


class SimpleMatcher(BaseMatcher):
    def __init__(self, source):
        super().__init__(source)

    def match_by_url(self, easy, hard):
        """
        Paths or URLs can be passed. URLs are converted into paths.
        """
            
        if easy.startswith(("www", "https://")) and hard.startswith(("www", "https://")):
            easy = self.data_handler.search_by("e", "url", easy)
            hard = self.data_handler.search_by("h", "url", hard)
        else:
            raise Exception("You did not provide a valid URL to match_by_url in SimpleMatcher.py")
        
        if easy is None or hard is None:
            logging.error(f"SimpleMatcher: Could not match {easy} with {hard}")
            return
        
        logging.info(f"SimpleMatcher: Writing Match: {easy} with {hard}")
        self.write_match(easy, hard)
        

            