Das Skript ```scrape_InstaCaptions.py``` ist ein an den ```BaseScraper``` angelehnter Web-Scraper, der speziell für Instagram Captions von Nachrichtenleicht entwickelt wurde. Es verwendet die ```instaloader``` Bibliothek, um Daten von Instagram zu extrahieren. Dies ist eine der wenigen Insta Bibliotheken, die zuverlässig funktionieren und auch nicht gesperrt werden, da kein Login benötigt wird. Der Scraper funktioniert außerdem auch für vergangene Posts und speichert nur die neusten ab. Die Hauptfunktionen des Skripts sind:

- Extrahieren von Metadaten und Inhalten von Instagram-Posts
- Extrahieren von Text als Titel aus den dazugehörigen Insta-Bildern
- Bereinigen des extrahierten Textes

```clean_text(text)```: Diese Funktion bereinigt den gegebenen Text, in unserem Fall immer die extrahierten Texte für den Titel. Sie entfernt nicht-alphanumerische Zeichen, begrenzt den Text auf die ersten 10 Wörter und entfernt Wörter, die vollständig in Großbuchstaben geschrieben sind. Hiermit wird ein gewisser Standard für die Titel erzeugt, damit die Ordner für die Speicherung übersichtlich bleiben

```text_from_image(url)```: Diese Funktion extrahiert Text aus einem Bild, das sich an der gegebenen URL befindet, in unserem Fall die URLs zu den Instagram-Bildern. Sie verwendet die ```pytesseract``` Bibliothek, um Text aus dem Bild zu extrahieren, und die ```clean_text Funktion```, um den extrahierten Text zu bereinigen. ```pytesseract``` ermöglicht die erkennung durch OCR (Optical Character Recognition) mit Kantenerkennungsalgorithmen aus der Computervision.

```base_metadata_dict(post)```: Diese Funktion erstellt ein Dictonary im Standardformat von allen Scraper mit Metadaten für einen gegebenen Instagram-Post. Die Metadaten enthalten den Titel (extrahiert aus dem Bild des Posts), die Beschreibung (die Bildunterschrift des Posts), die URL des Posts, das Datum des Posts und die Hashtags aus der Bildunterschrift des Posts.

```InstaScraper```: Ist eine Klasse, die von der ```BaseScraper``` Klasse erbt. Sie initialisiert einen ```instaloader.Instaloader``` und ein Instagram-Profil für den Benutzernamen "nachrichtenleicht". Die ```scrape``` Methode dieser Klasse durchläuft alle Posts des Profils und speichert die Metadaten und den Inhalt der Posts, die noch nicht gespeichert wurden. Bildunterschriften, die mit "Unser" beginnen sind immer Informationsposts und werden daher nicht gespeichert.

```main```: Das Hauptprogramm initialisiert einen InstaScraper und ruft seine scrape Methode auf, um das Scraping zu starten. Es konfiguriert auch das Logging, um Informationen über den Fortschritt des Scrapings im Terminal zu protokollieren.