## TF-IDF

Für das Matching der Artikel wurde das Tf-idf-Maß (Term Frequency - Inverse Document Frequency) verwendet, ein weit verbreitetes Verfahren im Bereich der Informationsretrieval und Textanalyse. Der Prozess umfasst folgende Schritte:

1. Vektorisierung des Artikels
2. Transformation in die Tf-idf Darstellung
3. Vergleich der Artikel-Vektoren mit Cosine-Similarity
4. Evaluation des Matchers mit zusätzlichen Kriterien

Zur Vektorisierung wurde eine Klasse auf Basis der sklearn API entwickelt, um den Tokenisierungsprozess vollständig zu kontrollieren. Der Article Vectorizer arbeitet ähnlich wie der CountVectorizer. In der .fit()-Funktion wird das Vokabular aus dem Corpus erstellt und in eine Häufigkeitsmatrix umgewandelt.
Spezifische Preprocessing-Schritte und Tokenisierung für Nachrichtenartikel umfassen:

- Berücksichtigung von n-grams:
    Einbeziehung von Wortgruppen unterschiedlicher Länge
- Kombination segmentierter Wörter:
    Zusammenführung für die leichte Sprache typischerweise segmentierter Wörter
- Extraktion von Substantiven und Eigennamen
    naives named entity recognition
- Einheitliche Kleinschreibung:
    Umwandlung aller Wörter Kleinbuchstaben am Ende aller Preprocessing-Schritte
- Ein- und Ausschluss von Zahlen


Eine sklearn Pipeline wurde genutzt, um die vektorisierten Artikel mit dem TfidfTransformer zu verarbeiten. Die Tf-idf-Matrix des gesamten Korpus wurde mittels Cosine Similarity bewertet, und der Artikel mit dem höchsten Score wird als Matches identifiziert.

Der aktuelle Stand erlaubt die Definition eines Matchers, der das Preprocessing durch den Article Vectorizer und das Matching zwischen leichten und schweren Artikeln ermöglicht. Weitere artikelbezogene Matching-Kriterien könnten implementiert werden:

- Berücksichtigung des Veröffentlichungsdatums
    - Maximale Differenz
    - time-decay in Evaluation
- Zeitrahmen des Korpus
    Einschränken des Zeitraums, aus dem Artikel stammen
- Vokabularbeschränkung (z.B. nur NL- bzw. DLF-Artikel)
- Kombination aus Titel, Teaser, Beschreibung und Inhalt
- Berücksichtigung der Platzierung im Ranking
    - Auswahl aus den Score-Plätzen
    

Der zeitliche Rahmen des Projekts ermöglichte leider nicht die vollständige Entwicklung des Matchers. Zukünftig könnte der Matcher durch eine Ensemble-Methode verbessert werden. Es wäre sinnvoll, den Article Vectorizer mit verschiedenen Parametern und Datensätzen auf die zu matchenden Artikel anzuwenden und durch ein Voting-System den "passenden" Artikel auszuwählen.

Ein lernbarer Zusammenhang zwischen den Parameterkonfigurationen und der Genauigkeit der einzelnen Matcher könnte hergestellt werden. Ein naiver Ansatz wäre Soft Voting, aber auch lineare Regression könnte als Evaluationsmethode dienen. Zum Trainieren eines solchen Modells könnte der bereits gematchte Datensatz der MDR-Artikel verwendet werden, da hier eine bijektive Zuweisung besteht.

Zusammengefasst bietet dieser Ansatz eine flexible und anpassbare Methode zur Artikelverarbeitung und -matching, die durch weitere Verfeinerungen und die Implementierung zusätzlicher Kriterien noch präziser und leistungsfähiger gemacht werden kann.
