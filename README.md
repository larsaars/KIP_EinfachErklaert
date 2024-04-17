# KIP_EinfachErklaert

## TODO

- Scraper für verschiedene Seiten
- Wie Audios speichern? -> erstmal nicht speichern
- Schema für Matching überlegen
- Rechereche zu Nachrichtenquellen
- Historischer vs aktueller Scraper

## Prozess
Die Idee ist es zunächst, eine Datenbank zu bauen. Dafür sollen wir uns nach Möglichkeit auch mit der anderen Gruppe, die das gleiche Projekt macht, zusammenschließen, damit keine doppelte Arbeit geschieht. Sobald wir die Daten haben, haben wir viel Freiraum, was wir machen könnten. Ein Vorschlag von Prof. Baumann war eine Coreference Analysis (gucken, was Bezüge sind "er"->"der Innenminister", wie gut funzt das bei leichter, wie gut bei schwerer Sprache, wie kann man ein einfaches Modell ausweiten angewandt auf schwerer Sprache), diesen Teil können wir uns aber in der "Forschungsphase" des Projekts noch überlegen.

### Ordnerschema

```
einfacherklaert/
├─ deutschlandfunk/
│  ├─ easy/
│  │  ├─ article-abcdef/
│  │  │  ├─ content.txt
│  │  │  ├─ audio.mp3
│  │  │  ├─ metadata.json
│  │  ├─ article-ghasdf/
│  │  
│  ├─ hard/
│  │  ├─ article-sdfdgd/
│  │  │  ├─ content.txt
│  │  │  ├─ audio.mp3
│  │  │  ├─ metadata.json
├─ matchings.txt

```

Dabei kann `matchings.txt` die Relationen zwischen article ids herstellen. Wir verwenden eine Ordnerstruktur, da plain files einfacher zu benutzen sind und nicht "altern".

### Scraper

Die Daten dieser Datenbank werden mithilfe von scrapern verschiedener Quellen gesammelt. Es reicht, wenn Artikel gleicher Organisationen gemacht werden. Also:

- [nachrichtenleicht](https://nachrichtenleicht.de) und [deutschlandfunk](https://deutschlandfunk.de)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) und [MDR](https://www.mdr.de/nachrichten/index.html)
- 
Es soll jeweils zu jeder Quelle im Optimalfall einen scraper geben, der historische Daten sammelt, und einer der laufen gelassen werden kann in Zukunft, wenn neue Artikel gepublisht werden.

### Matchen von normalen und leichten Artikeln (KI-Anteil)

Wir können hierfür verwenden, was wir wollen.

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
- Vielleicht Bildähnlichkeiten

## FAQ

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

- X MDR -> teilweise link zum original aber vom radio (nur audio) 
- X NDR -> nicht so nice/ kein feed

## zu Besprechen im nächsten Meeting
- reduzierung von gescrapten artikeln, für kürzere Laufzeit später
- Data Handler
- E-Mail