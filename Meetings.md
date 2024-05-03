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
    + Einleitung {Ben}
    + Allgemein
        + Herausforderungen {Felix}
        + Projektmanagment {Lars}
    + Was bisher geschah/ Aktueller Stand
        + DONE Scraper {Lars + Simon} 
        + DONE Datenstruktur {Felix} 
        + Kommunikation mit Nachrichtenquellen {Ben}
        + Über den KI-Server -> Mi auf Server {Ben} 
    + Ziele für zweite Hälfte
        + Matching {Ben}
            + Base und SimpleMatcher {Felix}
            + named entity recognition {Ben}
            + BERT {Ben}
            + Suche auf HuggingFace? {Ben}
        + Verbessungspunkte {Simon}
            + Risikos/ Zukünftige Herausforderungen 
                + Historische Artikel {Simon}
                + Skalierbarkeit des Projekt (DataHandler bei vielen Daten) {Simon}
                + MDR Scraper geht nur über UI {Lars}
- Präsentation: PowerPoint
    + alle Zoom Präsentation? -> Felix frägt
- nächstes Meeting vorgezogen auf Montag 06.05. 9:00Uhr
- Ben: Update DLF Kommunikation 
- evtl. Gespräch mit Prof. Baumann

## Meeting 06.05.24
- MDR nicht WDR im Rewview?!?