#!/usr/bin/env python3

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BING_KEY = os.getenv('BING_KEY').strip()

# Bing Search API key and URL
search_url = "https://api.bing.microsoft.com/v7.0/search"
search_term = 'intext:"Hier können Sie diese Nachricht auch in schwerer Sprache lesen:" site:mdr.de'

# Define the start and end dates
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 6, 30)

# Function to generate date ranges
def generate_date_ranges(start, end, delta):
    current = start
    while current < end:
        next_date = current + delta
        yield current, next_date - timedelta(days=1)
        current = next_date

# Generate 3-month date ranges
date_ranges = list(generate_date_ranges(start_date, end_date, timedelta(days=30)))

print(date_ranges)

headers = {"Ocp-Apim-Subscription-Key": BING_KEY}
links = set()

for start, end in date_ranges:
    params = {
        "q": search_term,
        "textDecorations": True,
        "textFormat": "HTML",
        "mkt": "de-DE",
        "count": 50,
        "offset": 0,
        "freshness": f"{start.strftime('%Y-%m-%d')}..{end.strftime('%Y-%m-%d')}"
    }

    while True:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        for result in search_results.get('webPages', {}).get('value', []):
            links.add(result['url'])

        if 'nextOffset' in search_results:
            params['offset'] = search_results['nextOffset']
        else:
            break

# Save the collected links to a file
with open('historic_mdr_easy_article_urls.txt', 'a') as file:
    for link in links:
        file.write(link + '\n')

print(f'Total links collected: {len(links)}')
