## TF-IDF

Für das Matching wurde ein Ansatz mit dem Tf-idf-Maß (term frequency - inverse document frequency) verfolgt. Dabei lässt sich die zugrundeliegende Idee in drei Teilschritte gliedern:

1. Vektorisierung des Artikels
2. Transformation in die Tf-idf Darstellung
3. Vergleich der Artikel-Vektoren mit Cosine-Similarity
4. Matcher evaluation with additional criteria

Für das Vektorisieren des Artikels wurde eine Klasse basierend auf der sklearn API definiert, um volle Kontrolle über den Tokenisierungsprozess zu gewährleisten. So konnten Nachrichtenartikel-spezifische Preprocessing Schritte implementiert werden. 

- segmentierte Wörter in zusammengesetzte Wörter umwandeln
- Isolierung von Substantiven und Nomen
- lowercasing nach Tokenization und n-gram generierung
- in-/exclution of numbers

Es wird eine sklearn Pipeline verwendet um die Vektorisierten Artikel mit dem TfidfTransformer in Reihe zu schalten. Die Tfidf-Matrix transformed auf dem gesamten Corpus (bzw Scope der zu vergleichenden Artikel) wird mit der cosine similarity ausgewertet und die jeweiligen Artikel mit dem höchsten score als das Match zurückgegeben

Im Matcher liesen sich weitere Artikel spezifische Matching-Kriterien implementieren:

- publishing date delta
    -> time-decay
- corpus scope
- vocabulary limitation (e.g. only NL-Artikel)
- combination of title, kicker, content

Der zeitliche Rahmen des Projekts hat leider nicht die Vervollständigung des Matchers hergegeben. Auf dem aktuellen Stand könnte mit einer Ensemble Methode aufgebaut werden.
Es bietet sich an die ArticleVectorizer mit unterschiedlichen Parametern und Daten-scopes auf die zu matchenden Artikel anzuwenden und durch ein Voting-System den "passenden" Artikel auszuwählen. 
Ein naiver Ansatz wäre SoftVoting, aber auch die Lineare Regression würde sich als Evaluationsmethode anbieten.
Zum Trainieren eines solchen Modells würde sich der bereits gematchte Datensatz der MDR Artikel anbieten, da hier bereits eine bijektive Zuweisung besteht.

