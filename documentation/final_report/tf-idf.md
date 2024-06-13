## TF-IDF

Für das Matching wurde ein Ansatz mit dem Tf-idf-Maß (term frequency - inverse document frequency) verfolgt. Dabei lässt sich die zugrundeliegende Idee in drei Teilschritte gliedern:

1. Vektorisierung des Artikels
2. Transformation in die Tf-idf Darstellung
3. Vergleich der Artikel-Vektoren mit Cosine-Similarity

Für das Vektorisieren des Artikels wurde eine Klasse basierend auf der sklearn API definiert, um volle Kontrolle über den Tokenisierungsprozess zu gewährleisten. So konnten Nachrichtenartikel-spezifische Preprocessing Schritte implementiert werden. 

- segmentierte Wörter in zusammengesetzte Wörter umwandeln
- Isolierung von Substantiven und Nomen
- lowercasing nach Tokenization und n-gram generierung
- in-/exclution of numbers
