## KIP_EinfachErklaert

### Table of contents
0. [TODO](#todo)
1. [Ordnerschema](#ordner)
2. [Prozess](#prozess)
3. [FAQ](#faq)

<a name="todo"></a>
### 0. TODO 

- Scraper für verschiedene Seiten
- Schema für Matching überlegen

<a name="ordner"></a>
### 1. Ordnerschema 

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

Dabei kann `matchings.txt` die Relationen zwischen article ids herstellen.

<a name="scraper"></a>
### 2. Scraper  

Es reicht, wenn Artikel gleicher Organisationen gemacht werden. Es soll jeweils zu jeder Quelle im Optimalfall einen scraper geben, der historische Daten sammelt, und einer der laufen gelassen werden kann in Zukunft, wenn neue Artikel gepublisht werden. 

Quellen:

- [nachrichtenleicht](https://nachrichtenleicht.de) und [deutschlandfunk](https://deutschlandfunk.de)
- [MDR: Leichte Sprache](https://www.mdr.de/nachrichten/podcast/leichte-sprache/nachrichten-leichte-sprache-100.html) und [MDR](https://www.mdr.de/nachrichten/index.html)

<a name="prozess"></a>
### 3. Prozess 

Die Idee ist es zunächst, eine Datenbank zu bauen. Dafür sollen wir uns nach Möglichkeit auch mit der anderen Gruppe, die das gleiche Projekt macht, zusammenschließen, damit keine doppelte Arbeit geschieht. Sobald wir die Daten haben, haben wir viel Freiraum, was wir machen könnten. Ein Vorschlag von Prof. Baumann war eine Coreference Analysis (gucken, was Bezüge sind "er"->"der Innenminister", wie gut funzt das bei leichter, wie gut bei schwerer Sprache, wie kann man ein einfaches Modell ausweiten angewandt auf schwerer Sprache), diesen Teil können wir uns aber in der "Forschungsphase" des Projekts noch überlegen.

<a name="faq"></a>
### 3. FAQ 

- Was ist die Abgabe? Datensatz? Scraping Tool? Matching Tool?
> abzugeben ist alles was wir machen, also so wie wir dachten das matching tool und auch noch alle modelle die danach entstehen sollten wir so weit kommen

- Soll eine KI Verarbeitung statt finden, oder nur Aufbau des Datensatzes egal wie?
> ja er meinte wir können alles was uns hilfreich erscheint mit einbeziehen und hält es auch mit KI für am schlausten
  
- Können wir unsere Datenbank auf dem (KI) Server laufen lassen?
> ja

- Sollen wir zwischen verschienen Seiten matchen, oder immer nur zwischen gleichen Anbieter (z.B Deutschlandfunk zu einfache Nachrichten).
> nein, nur die "anbieterpaare" also zb Nachrichten leicht und DF

- Soll der Scraper historische Daten abrifen oder immer nur die aktuellsten Artikel?
> beides wenn möglich, zwei einzelne scraper

- Wäre es ok wenn wir die Daten direkt anfragen ohne Scraping?
> ja, er meinte aber er hat da keine Hoffnungen, dass die uns das bereitstellen bzw überhaupt so sortiert haben, wie wir es bräuchten aber vielleicht haben wir ja glück