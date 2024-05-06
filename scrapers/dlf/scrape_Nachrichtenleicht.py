#!/usr/bin/env python3

"""
Scrapes the current articles from Nachrichtenleicht and saves them to the database.
"""

import sys
import os
import logging
import subprocess

# add git root dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append(subprocess.check_output('git rev-parse --show-toplevel'.split()).decode('utf-8').strip())

from scrapers.dlf.DLFScrapers import NachrichtenleichtScraper

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    NachrichtenleichtScraper().scrape()