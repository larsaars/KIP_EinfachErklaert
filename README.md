## KIP_EinfachErklaert

### General

Sources for the articles are:

- [Nachrichtenleicht](https://nachrichtenleicht.de), [Nachrichtenleicht auf Instagram](https://www.instagram.com/nachrichtenleicht/) and [Deutschlandfunk](https://deutschlandfunk.de)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) and [MDR](https://www.mdr.de/nachrichten/index.html)

![Pipeline](./documentation/images/pipe.png)

### Scraped Data

The [DataHandler](datahandler/DataHandler.py) module is responsible for managing the scraped data uniformly. The data is stored in following structure in the git root.

- data
    - Subfolder for each **News Source** (dlf, mdr)
        - **Matches** (links easy and hard versions)
        - Subfolders for **easy** and **hard** versions
            - **Lookup-File**
            - Folder for each **Article** (named after the publication date and title)
                - **Metadata**, **Content**, **Raw** (html), **Audio** (if available)

### Quickstart Guide
#### Installation
```bash
git clone https://github.com/larsaars/KIP_EinfachErklaert.git
cd KIP_EinfachErklaert
pip install -r requirements.txt
```

#### Scrapers
| **File**| **Functionality** |
----------|-------------------|
| [`scrapers/dlf/scrape_Deutschlandfunk.py`](scrapers/dlf/scrape_Deutschlandfunk.py)| Scrapes current articles from Deutschlandfunk.|
| [`scrapers/dlf/scrape_Nachrichtenleicht.py`](scrapers/dlf/scrape_Nachrichtenleicht.py)| Scrapes current articles from Nachrichtenleicht.|
| [`scrapers/dlf/scrape_InstaCaptions.py`](scrapers/dlf/scrape_InstaCaptions.py)| Scrapes Instagram captions and metadata from the "nachrichtenleicht" profile.|
| [`scrapers/mdr/current_news_scraper.py`](scrapers/mdr/current_news_scraper.py)| Scrapes current easy and hard articles from MDR.|
| [`scrapers/mdr/historic_news_scraper.py`](scrapers/mdr/historic_news_scraper.py)| Scrapes historic easy and hard articles from MDR.|
| [`matchers/SimpleMatcher.py`](matchers/SimpleMatcher.py) | Manually matches articles or checks the MDR match cache.|
| [`datahandler/reformat_date.py`](datahandler/reformat_date.py)| Renames directories by reformatting date strings in their names.|
| [`datahandler/DataHandler.py`](datahandler/DataHandler.py) | Handles reading, writing, and searching articles, including managing metadata, content, and audio files.|





