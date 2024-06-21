## KIP_EinfachErklaert

### General

This project was developed as part of the "KI-Projekt" course during the summer term of 2024 at OTH Regensburg by Ben, Felix, Lars and Simon. It is designed to be used for scientific research only. The goal of the project is to scrape and match german news articles from sources that provide content in both easy (in german: "leichte" or "einfache Sprache") and standard language. For simplicity, we refer to the articles as **easy** or **hard**. Currently supported sources for the articles are:

- [Nachrichtenleicht](https://nachrichtenleicht.de), [Nachrichtenleicht on Instagram](https://www.instagram.com/nachrichtenleicht/) (easy) and [Deutschlandfunk](https://deutschlandfunk.de) (hard)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) (easy) and [MDR](https://www.mdr.de/nachrichten/index.html) (hard)

The code is built modularly. Main modules are:

- [Scrapers](./scrapers/): scrape the data from the sources
- [DataHandler](./datahandler/): manages the scraped data uniformly and provides an interface for reading, writing, and searching the data
- [Matchers](./matchers/): matches corresponding articles one on one (easy to standard) from the same source. This is only a sneak peak on what could be possible
- [Gui App and audio transcriber](./gui_application/): a GUI application which can pick audios, transcribe them and detect certain characteristics of the audio that are relevant for the project

Modules may be used individually as needed. 

### Data Structure of Scraped Data

The project uses a custom data structure consisting of folders and files (txt, json, csv, html, mp3) to store the scraped data. The The data is stored in the git root directory like:

```
data/
├── <source>/ (dlf or mdr)
│   ├── matches_<source>.csv
│   ├── <language niveau>/ (easy or hard)
│   │   ├── lookup_<source>_<niveau>.csv
│   │   ├── 2023-06-01-Sample_Article/
│   │   │   ├── Metadata.json
│   │   │   ├── Content.txt
│   │   │   ├── Raw.html
│   │   │   └── Audio.mp3 (if available)
```

On runtime the data can be read into Pandas DataFrames with the DataHandler read capability.

### Developer Guide

#### Installation
```bash
git clone https://github.com/larsaars/KIP_EinfachErklaert.git
cd KIP_EinfachErklaert
pip install -r requirements.txt
```

#### Scrapers

The scrapers are designed to be executed on a regular basis (e.g., by weekly cron jobs on a server). The following table shows the most important scrapers with a short explanation and frequency:

| **File**| **Functionality** |
|---------|-------------------|
| [`scrapers/dlf/scrape_Deutschlandfunk.py`](scrapers/dlf/scrape_Deutschlandfunk.py)| Scrapes todays articles from Deutschlandfunk (hard)|
| [`scrapers/dlf/scrape_Nachrichtenleicht.py`](scrapers/dlf/scrape_Nachrichtenleicht.py)| Scrapes articles of several weeks (depending on how many articles specified in the api) from Nachrichtenleicht (easy)|
| [`scrapers/dlf/scrape_InstaCaptions.py`](scrapers/dlf/scrape_InstaCaptions.py)| Scrapes captions of all posts on the "nachrichtenleicht" Instagram profile and analyzes images for titles|
| [`scrapers/mdr/current_news_scraper.py`](scrapers/mdr/current_news_scraper.py)| Scrapes five days of articles easy and hard articles from MDR|
| [`scrapers/mdr/historic_news_scraper.py`](scrapers/mdr/historic_news_scraper.py)| Scrapes old easy and hard articles from MDR |

#### DataHandler

The DataHandler is not an executable but a module to use when further developing scrapers or matcher and dealing with data storage (read, write search). Examples how to use the DataHandler can be found [here](./datahandler/datahandler_examples.ipynb).







