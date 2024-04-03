# KIP_EinfachErklaert

## TODO

- Scraper für verschiedene Seiten
- Deutschlandfunk anschreiben
- Wie Audios speichern? -> erstmal nicht speichern
- Schema für Matching überlegen
- Aufgabe evaluieren -> Mit Prof sprechen
- Rechereche zu Nachrichtenquellen
- Historischer vs aktueller Scraper
- SQL Datenbank aufbauen -> OTH Postgres
- zusammenschliessen mit der anderen Gruppe

## Prozess
Die Idee ist es zunächst, eine Datenbank zu bauen. Dafür sollen wir uns nach Möglichkeit auch mit der anderen Gruppe, die das gleiche Projekt macht, zusammenschließen, damit keine doppelte Arbeit geschieht. Nachdem die Datenbank erstellt wurde, sollen wir noch Passagen

### Datenbank
Eine Datenbank (wie Postgres) an sich sollen wir nicht anlegen; sondern ein Ordnerschema, z.B.:

```
einfacherklaert/
├─ easy/
│  ├─ article-abcdef/
│  │  ├─ content.txt
│  │  ├─ audio.mp3
│  │  ├─ metadata.json
│  ├─ article-ghasdf/
├─ hard/
│  ├─ article-sdfdgd/
│  │  ├─ content.txt
│  │  ├─ audio.mp3
│  │  ├─ metadata.json
├─ matchings.txt
```

Dabei kann `matchings.txt` die Relationen zwischen article ids herstellen. Wir verwenden eine Ordnerstruktur, da plain files einfacher zu benutzen sind und nicht "altern".


### Matchen von normalen und leichten Artikeln

- Metadata
	+ Datetime of Release
	+ Headline
	+ Author
	+ Imageurl
	+ Audiourl
- Text of the Article
- Short Description
- Datetime of Scraping
- Source
- ID of Scraper

## Eigene Datenbank für Verknüfung leicht zu schwer


## Fragen und Antworten

- Was ist die Abgabe?
	+ Datensatz?
	+ Scraping Tool?
	+ Matching Tool?
-> abzugeben ist alles was wir machen, also so wie wir dachten das matching tool und auch noch alle modelle die danach entstehen sollten wir so weit kommen

- Soll eine KI Verarbeitung statt finden, oder nur Aufbau des Datensatzes egal wie?
-> ja er meinte wir können alles was uns hilfreich erscheint mit einbeziehen und hält es auch mit KI für am schlausten
  
- Können wir unsere Datenbank auf dem (KI) Server laufen lassen?
-> ja
- Sollen wir zwischen verschienen Seiten matchen, oder immer nur zwischen gleichen Anbieter (z.B Deutschlandfunk zu einfache Nachrichten).
-> nein, nur die "anbieterpaare" also zb Nachrichten leicht und DF
- Soll der Scraper historische Daten abrifen oder immer nur die aktuellsten Artikel?
-> beides wenn möglich, zwei einzelne scraper
- Wäre es ok wenn wir die Daten direkt anfragen ohne Scraping?
-> ja, er meinte aber er hat da keine Hoffnungen, dass die uns das bereitstellen bzw überhaupt so sortiert haben, wie wir es bräuchten aber vielleicht haben wir ja glück
