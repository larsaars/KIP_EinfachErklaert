## KIP_EinfachErklaert

### 1. Datenstruktur  
In folgender Ordnerstruktur werden die Daten der Scraper gespeichert. Die einheitliche Verwaltung der Daten übernimmt das Modul [DataHandler](services/DataHandler.py)

- data
    - Unterorder für jede **Nachrichtenquelle** (dlf, mdr)
        - **Matches** (verbindet easy und hard)
        - Unterordner für **easy** und **hard**
            - **Lookup-File**
            - Ordner für jeden **Artikel** (benannt nach Erscheinungsdatum und Titel.)
                - **Metadaten**, **Content**, **Raw** (html), **Audio** (wenn verfügbar)

### 2. Quellen  

- [nachrichtenleicht](https://nachrichtenleicht.de) und [deutschlandfunk](https://deutschlandfunk.de)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) und [MDR](https://www.mdr.de/nachrichten/index.html)

### 3. FAQ 

- Was ist die Abgabe? Datensatz? Scraping Tool? Matching Tool?
> abzugeben ist alles was wir machen, also so wie wir dachten das matching tool und auch noch alle modelle die danach entstehen sollten wir so weit kommen

- Soll eine KI Verarbeitung statt finden, oder nur Aufbau des Datensatzes egal wie?
> ja er meinte wir können alles was uns hilfreich erscheint mit einbeziehen und hält es auch mit KI für am schlausten  

- Sollen wir zwischen verschienen Seiten matchen, oder immer nur zwischen gleichen Anbieter (z.B Deutschlandfunk zu einfache Nachrichten).
> nein, nur die "anbieterpaare" also zb Nachrichten leicht und DF

- Soll der Scraper historische Daten abgreifen oder immer nur die aktuellsten Artikel?
> beides wenn möglich, zwei einzelne scraper





