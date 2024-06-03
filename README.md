## KIP_EinfachErklaert

### General

This project was developed as part of the "KI-Projekt" course during the summer term of 2024 at OTH Regensburg. It is designed to be used for scientific research. The goal of the project is to scrape and match german news articles from sources that provide content in both easy (in German: "leichte" or "einfache Sprache") and standard language. For simplicity, we refer to the articles as **easy** or **hard**. Currently supported sources for the articles are:

- [Nachrichtenleicht](https://nachrichtenleicht.de), [Nachrichtenleicht on Instagram](https://www.instagram.com/nachrichtenleicht/) (easy) and [Deutschlandfunk](https://deutschlandfunk.de) (hard)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) (easy) and [MDR](https://www.mdr.de/nachrichten/index.html) (hard)

The project is built modularly. Main modules are:

- [Scrapers](./scrapers/): scrape the data from the sources
- [DataHandler](./datahandler/): manages the scraped data uniformly and provides an interface for reading, writing, and searching the data
- [Matchers](./matchers/): match corresponding articles (easy to standard) from the same source

Modules may be used individually as needed. The current simplified pipeline is:

![Pipeline](./documentation/images/pipe.png)

### Data Structure of Scraped Data

The project uses a custom data structure consisting of folders and files (txt, json, csv, html, mp3) to store the scraped data. The data is stored in the git root directory like:

- data
    - Subfolder for each **News Source** (dlf, mdr)
        - **Matches** (csv, that links easy and hard versions)
        - Subfolders for **easy** and **hard** versions
            - **Lookup-File** (csv, containig url and path for quick search)
            - Folder for each **Article** (named after the publication date and title)
                - **Metadata** (json), **Content** (txt), **Raw** (html), **Audio** (mp3, if available)

### User Guide
#### Installation
```bash
git clone https://github.com/larsaars/KIP_EinfachErklaert.git
cd KIP_EinfachErklaert
pip install -r requirements.txt
```

In the follwing some further explanation on the modules.
#### Scrapers

Scrapers
The scrapers are designed to be executed on a regular basis (e.g., by weekly cron jobs on a server). The following table shows the most important scrapers with a short explanation and frequency:

| **File**| **Functionality** |
|---------|-------------------|
| [`scrapers/dlf/scrape_Deutschlandfunk.py`](scrapers/dlf/scrape_Deutschlandfunk.py)| Scrapes last week's articles from Deutschlandfunk (hard)|
| [`scrapers/dlf/scrape_Nachrichtenleicht.py`](scrapers/dlf/scrape_Nachrichtenleicht.py)| Scrapes last week's articles from Nachrichtenleicht (easy)|
| [`scrapers/dlf/scrape_InstaCaptions.py`](scrapers/dlf/scrape_InstaCaptions.py)| Scrapes captions of all posts on the "nachrichtenleicht" Instagram profile and analyzes images for titles|
| [`scrapers/mdr/current_news_scraper.py`](scrapers/mdr/current_news_scraper.py)| Scrapes current easy and hard articles from MDR|
| [`scrapers/mdr/historic_news_scraper.py`](scrapers/mdr/historic_news_scraper.py)| Scrapes historic easy and hard articles from MDR |

#### DataHandler
The DataHandler is not an executable but a module to use when further developing scrapers or matcher and dealing with data storage (read, write search). Examples how to use the DataHandler can be found [here](./datahandler/datahandler_examples.ipynb).

#### Matchers
Work in progress








