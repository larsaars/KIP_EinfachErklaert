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

## Meeting 15.05.24
- Fehler im Data Handler beheben 
- Themen für Austausch mit anderer Gruppe
    - Daten zusammenfügen ?!?
    - Fachlicher Austausch Scraper
    - Gemeinsame Ideen für Matcher
- Anmerkungen aus Präsentation
    - Datumsformat ändern weil besser für Sortierung -> yyyy-MM-dd
        - Script was bestehende DLF Ordner und Metadaten umbennent 
    - html noch mit scrapen -> raw.html
    - Instagram captions scraping
    - MDR hist daten
- Austausch mit anderer Gruppe und Prof Baumann
    - Anmerkungen Prof Baumann
        - Ein einheitliches Projekts -> Daten auf den Server zusammenführen
        - Raw (html) Datei speichern
        - Bei Ordnerstruktur bleiben (auch wegen Audio)
        - MP3 runter laden
        - Zusammenbinden der Paare
        - Gruppen könnten differieren in der Art was man mit den Daten macht
        - Kein Gatekeeping zwischen Gruppen
        - Absprache über Schnittstellen
- Beide Gruppen benutzen Datahandler 
- Einführung KIGS für andere Gruppe

## Meeting 22.05.24
- Themen
    - Ideen wie wir wieder Struktur rein bringen können
    - Pläne fürs weitere Vorgehen
- Besprochen
    - Datensätze von DLF und Nachrichten Leicht verbinden -> Kombination aus mehreren Dingen: Stichworte, Metadaten (BERT)
    - Was machen wir mit den MDR Daten?
    - MDR ist bereits gematcht -> Testmenge
- Aufgaben für nächste Woche
    - Lars: Historischer MDR Scraper
    - Felix: Check MDR matches; Matches mit [Sklearn](!matchers/_ideas/sklearn_matcher.py) möglich? 
    - Ben: Logging in File schreiben; Insta captions scrapen; Matching über Keywords ohne KI
    - Simon: Matching approaches anschauen allgemein; DLF <-> NL händisch als Testdaten matchen
    - 
## Meeting 30.05.24

- Präsentieren von Ergebnissen die Woche:
    - Felix:
        - Repo aufgeräumt
        - Problem mit SKLearn Matching Ansatz
    - Simon: sein Matching Ansatz
    - Lars: MDR scraper erklären und Fehler mit Felix besprechen
    - Ben:
        - Instagram Captions Scraper
        - Keyword Extraction als Matching Ansatz funktioniert schlecht
- Ziele bis zum Ende:
    - Datenbank joinen mit anderem Team (sie machen das auch mit dem DataHandler) (sprechen mit Baumann nächsten Montag)
    - Matchings testen
          - LLM (Ben und Lars)
          - TF-IDF (Simon)
          - irgendwas anderes DL (N/A)
    - Dokumentation oder QuickStart schreiben (Felix)
    - Poster (LibreOffice, mit Vorlage) und Abschlussbericht (letzte 2 Wochen)
- Aufgaben für nächste Woche:
    - Felix: QuickStart guide fürs Repo schreiben im README, DataHandler Pfade zu ASCII und Texte zu UTF8
    - Lars: MDR scraper komplett zum laufen bringen (historischen laufen lassen, current scraper verbinden mit SimpleMatcher, keep saving easy articles without match)
    - Simon: TF-IDF Matching Ansatz verfolgen
    - Ben: seine Ansätze
    - Ben, Simon, Lars: zum Baumann: andere Gruppe wir haben Kontakt gesucht, LLM Ansatz, DL andere Ansatz? hilf uns Baumann!
    - Ben und Lars: LLM learning ansatz zum matchen (bzw. was der Baumann eben gesagt hat beim Treffen)




