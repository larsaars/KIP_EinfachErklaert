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

## Datenbank Schema 
-> Für Artikel
-> Eine für leicht eine für schwer

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


## Fragen

- Was ist die Abgabe?
	+ Datensatz?
	+ Scraping Tool?
	+ Matching Tool?
- Soll eine KI Verarbeitung statt finden, oder nur Aufbau des Datensatzes egal wie?
- Können wir unsere Datenbank auf dem (KI) Server laufen lassen?
- Sollen wir zwischen verschienen Seiten matchen, oder immer nur zwischen gleichen Anbieter (z.B Deutschlandfunk zu einfache Nachrichten).
- Soll der Scraper historische Daten abrifen oder immer nur die aktuellsten Artikel?
- Wäre es ok wenn wir die Daten direkt anfragen ohne Scraping?
