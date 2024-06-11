#!/usr/bin/env python3

"""This file is only intended to be run one time to use the serpapi Google search API to scrape the historic article urls of MDR"""

import serpapi 
import json
import sys

def main():
    search_offset = 0

    # let run until it fails!
    # (either because api key is invalid or because the search results are exhausted)
    while True:
        # define the search parameters
        params = {
            "api_key": "",  # TODO replace with your own API key
            "engine": "google",
            "q": 'intext:"Hier können Sie diese Nachricht auch in schwerer Sprache lesen:" site:mdr.de',
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
            "start": search_offset,
            "num": "100"
        }


        results = serpapi.search(params).as_dict()


        # update offset and total results
        search_offset += 100


        # get and print the urls from the results to stdout
        for result in results['organic_results']:
            print(result['link'])


if __name__ == '__main__':
    main()
