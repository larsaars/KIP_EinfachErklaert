## Meeting 03.04.24

- TODOs
- Fragen Für Gespräch mit Prof. Baumann
- Datenbank Schema
- Informationsaustausch um alle auf den gleichen Stand zu bringen


## Meeting 10.04.24

- Repo jetzt privat
- Simon stellt Scraper für Deutschlandfunk/ Nachrichtenleicht vor
- Festlegen auf Ordnerstrukur für die Speicherung der gescrapten Artikel
    + Benennung der Ordner
- Vorläufiges Festlegen der Datenquellen
    + Deutschlandfunk/ Nachrichtenleicht
- Aufgabenteilung bis nächste Woche
    + Very basic Interface/ Handler für Ordnerstruktur -> Felix
    + Zweite Datenquelle raussuchen -> Ben
    + Zusammenschliessen mit der anderen Gruppe -> Ben
    + Scraper aktuelle Artikel deutschlandfunk finalsieren -> Simon
    + Scraper für historische Artikel deutschlandfunk -> Lars
    + Scraper für historische Artikel nachrichtenleicht -> Lars

## Meeting 17.04.24

- DataHandler Vorstellung
- Historischer Scraper Deutschlandfunk: Abwarten auf E-Mail Antwort warten
- Lookup Table für gescrapte Artikel um abgleichen zu können ob de Artikel schon gecraped wurde -> Url ändert sich
- Zweite Nachrichtenquelle: MDR
- Midterm Review 08.05
- Aufgabenteilung bis nächste Woche:
    + Data Handler weiter ausbauen, besonders in Verbindung mit Scraper -> Felix
    + Aktueller Scraper MDR -> Lars
    + Kommunikation mit anderer Gruppe -> Ben
    + Deutschlandfunk Kontakt -> Ben
    + Data Handler und Scraper auf KIS aufsetzen -> Ben
    + MDR schreiben -> Ben
    + Deutschlandfunk Scraper ausbauen -> Simon

## Meeting 24.04.24

- Midterm Review
    - Struktur:
        - Problemstellung
        - Herausforderungen
        - "Projektmanagment"
        - Über den KI-Server
        - Wie haben wir angefangen
        - Ansätze (Scraper {Lars + Simon}, DataHandler + Dateisystem {Felix, 2S})
        - Kommunikation mit Nachrichtenquellen {Ben}
        - Aktueller Stand
        - Ziele für zweite Hälfte
        - Verbessungspunkte
    - Format: Markdown
- Vorstellung Projekte von letzter Woche
    - Lars: MDR scraper
    - Felix: DataHandler
- Aufgabenteilung bis nächste Woche:
    - Lars: MDR Scraper fertig + Bericht
    - Felix: DataHandler ausbauen (save_matching + bessere read funktion) + Bericht
    - Simon: Deutschlandfunk Scraper fertig + Bericht
    - Ben: Basic matching Struktur + Bericht
- Für Meeting nächste Woche
    - Midterm Review (was würde schon geschrieben, was müssen wir noch machen)
    - Felix (29.04): MidtermReview evtl doch LaTeX (zB keine guten Bildunterschriften in Markdown)

## Meeting 30.04.24

- Lars: 
    + DataHandler sollte vielleicht nicht das Datum formatieren
    + Mechanismus einbauen, der versichert, dass der data Ordner auf root Ebene des Projektes speichert.
- MDR Scraper (Audio Download schwierig)
- BaseMatcher und SimpleMatcher
- Aufteilung von MidtermReview {10 Seiten, 2.5 p.P.}
    + TODO Einleitung {Ben}
    + Allgemein
        + DONE Herausforderungen {Felix}
        + DONE Projektmanagment {Lars}
    + Was bisher geschah/ Aktueller Stand
        + DONE Scraper {Lars + Simon} 
        + DONE Datenstruktur {Felix} 
        + DONE Kommunikation mit Nachrichtenquellen {Ben}
        + DONE Über den KI-Server -> Mi auf Server {Ben} 
    + Ziele für zweite Hälfte
        + Matching {Ben}
            + DONE Base und SimpleMatcher {Felix}
            + DONE named entity recognition {Ben}
            + TODO BERT {Ben}
            + DONE Suche auf HuggingFace? {Ben}
        + Verbessungspunkte {Simon}
            + Risikos/ Zukünftige Herausforderungen 
                + DONE Historische Artikel {Simon}
                + DONE Skalierbarkeit des Projekt (DataHandler bei vielen Daten) {Simon}
                + DONE MDR Scraper geht nur über UI {Lars}
- Präsentation: PowerPoint
    + alle Zoom Präsentation? -> Felix frägt
- nächstes Meeting vorgezogen auf Montag 06.05. 9:00Uhr
- Ben: Update DLF Kommunikation 
- evtl. Gespräch mit Prof. Baumann

## Meeting 06.05.24

### Midterm
+ TODO Einleitung {Ben}
+ Allgemein
    + DONE Herausforderungen {Felix}
    + DONE Projektmanagment {Lars}
+ Was bisher geschah/ Aktueller Stand
    + DONE Scraper {Lars + Simon} 
    + DONE Datenstruktur {Felix} 
    + DONE Kommunikation mit Nachrichtenquellen {Ben}
    + DONE Über den KI-Server -> Mi auf Server {Ben} 
+ Ziele für zweite Hälfte
    + Matching {Ben}
        + DONE Base und SimpleMatcher {Felix}
        + DONE named entity recognition {Ben}
        + TODO BERT {Ben}
        + DONE Suche auf HuggingFace? {Ben}
    + Risikos/ Zukünftige Herausforderungen 
        + DONE Historische Artikel {Simon}
        + DONE Skalierbarkeit des Projekt (DataHandler bei vielen Daten) {Simon}
        + DONE MDR Scraper geht nur über UI {Lars}

### Präsentation (max. 20 min)
- Zuständigkeit
    + Ben: Nachrichtenquellen + Ausblick (Matching) + Einleitung
    + Simon: DLR Scraper
    + Lars: MDR Scraper + Pipeline
    + Felix: Datahandler + organisatiorische Herausforderungen

- Reihenfolge:
    + Einleitung
        + Wie sind wir auf die Quellen gekommen
        + Kommunikation?
    + Pipeline
    + Datahandler: nur sagen dass es unser Interface ist
    + Scraper
        + DLF
        + MDR
    + Matcher
 
- Felix Teil (seperat):
    + organisatorische herausforderungen
    + DataHandler

- Morgen Meeting: 14:00Uhr?
    + Review und Präsi? zusammenfügen

## Meeting 07.05.24

## Meeting 15.05.24
- Datumsformat ändern weil besser für sortierung
- Fehler bei DLF Scraper beheben, bzw im Data Handler
- benreher@im-kigs:/data/projects/einfach/KIP_EinfachErklaert/scrapers/dlf$ python3 scrape_Deutschlandfunk.py 
Traceback (most recent call last):
  File "/data/projects/einfach/KIP_EinfachErklaert/scrapers/dlf/scrape_Deutschlandfunk.py", line 19, in <module>
    DeutschlandfunkScraper().scrape()
  File "/data/projects/einfach/KIP_EinfachErklaert/scrapers/dlf/DLFScrapers.py", line 66, in scrape
    if not self.data_handler.is_already_saved(self.difficulty_level, article_url):
  File "/data/projects/einfach/KIP_EinfachErklaert/services/DataHandler.py", line 137, in is_already_saved
    if self.search_by(dir, "url", url) == None:
  File "/data/projects/einfach/KIP_EinfachErklaert/services/DataHandler.py", line 111, in search_by
    return self.helper._search_url_in_lookup(dir, attribute_value)
  File "/data/projects/einfach/KIP_EinfachErklaert/services/DataHandler.py", line 265, in _search_url_in_lookup
    res = df.loc[df["url"].str.contains(url), "path"]
  File "/usr/lib/python3/dist-packages/pandas/core/indexing.py", line 925, in __getitem__
    return self._getitem_tuple(key)
  File "/usr/lib/python3/dist-packages/pandas/core/indexing.py", line 1100, in _getitem_tuple
    return self._getitem_lowerdim(tup)
  File "/usr/lib/python3/dist-packages/pandas/core/indexing.py", line 862, in _getitem_lowerdim
    return getattr(section, self.name)[new_key]
  File "/usr/lib/python3/dist-packages/pandas/core/indexing.py", line 931, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/usr/lib/python3/dist-packages/pandas/core/indexing.py", line 1143, in _getitem_axis
    elif com.is_bool_indexer(key):
  File "/usr/lib/python3/dist-packages/pandas/core/common.py", line 139, in is_bool_indexer
    raise ValueError(na_msg)
ValueError: Cannot mask with non-boolean array containing NA / NaN values
- html noch mit scrapen, response in textfile speichern 
