# Nachrichtenangebote

## Deutschlandradio

- Teil des öffentlich-rechtlichen Rundfunks
- Produziert Deutschlandfunk und Nachrichtenleicht
- Breite inhaltliche Abdeckung
- Redaktionelle Nähe zwischen Deutschlandfunk und Nachrichtenleicht
- Inhalte von Menschen erstellt

### Nachrichtenleicht

- Veröffentlicht wöchentlich 5-6 Artikel in leichter Sprache
- Auch als Audio verfügbar
- Menschliche Sprecher

## Weitere Nachrichtenangebote 

- APA, NDR und SR in Betracht gezogen
- APA von capito.ai generierte Texte, keine Audioversionen
- NDR und SR bieten leicht verständliche Nachrichten mit Audio an
    -> formell und inhaltlich stark abweichend von DLF und MDR

# Scraping DLF

- DeutschlandradioScraper als Basis
- Strukturelle Ähnlichkeit zwischen DLF und NL
- Unterschiede in Metadaten und Audioverfügbarkeit
- API-Schnittstelle für Nachrichtenleicht-Feed



# Herausforderungen

## Scraper 

- Websites werden kontinuierlich aktualisiert und verbessert
- Änderungen in HTML-Struktur und CSS-Klasssen können Scraping-Skripte beeinträchtigen
- Regelmäßige Überwachung und Aktualisierung der Skripte erforderlich

## Skalierbarkeit

- Verarbeitung großer Datenmengen mit dem DataHandler 
- Nicht speziell für Operationen auf großen Datenmengen optimiert
- Optimierungsmöglichkeiten:
    - Parallelisierung
    - Optimierung der Daten-/ Ordnerstruktur
    - Nutzung eines dedizierten Datenbanksystems

## Historische Artikel

- Herausforderung beim Scraping
- Zugänglichkeit und Verfügbarkeit von URLs
- Gewährleistung der Konsistenz der gesammelten Daten 
    -> Implementierung von Versionierung der Artikel im DataHandler
