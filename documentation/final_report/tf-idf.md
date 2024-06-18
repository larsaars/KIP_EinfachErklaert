## Matching

Für das Matching der Artikel wurde das Tf-idf-Maß (Term Frequency - Inverse Document Frequency) verwendet, ein weit verbreitetes Verfahren im Bereich der Informationsretrieval und Textanalyse. Sie dient dazu, die Bedeutung eines Wortes in einem Dokument relativ zu einer Sammlung von Dokumenten (Korpus) zu bewerten. Der Prozess umfasst folgende Schritte:

1. Vektorisierung des Artikels
2. Transformation in die Tf-idf Darstellung
3. Vergleich der Artikel-Vektoren mit Cosine-Similarity
4. Evaluation des Matchers mit zusätzlichen Kriterien

### ArticleVectorizer

Die Transformer-Klasse `ArticleVectorizer` implementiert eine Textvektorisierungsfunktion, die speziell für die Verarbeitung von Texten in einfacher Sprache entwickelt wurde. Die Klasse implementiert anwendungsspezifische Funktionen und dient dazu Texte zu verarbeiten und sie in ein Format zu transformieren, das für maschinelles Lernen verwendet werden kann.
Die Klasse verwendet die Natural Language Toolkit (NLTK) Bibliothek um Stoppwörter für Deutsch zu laden und die Tokenisierung durchzuführen.

#### Funktionsweise

1. **Tokenisierung und Bereinigung:** Die Methode `generate_tokens` ist dafür verantwortlich, einen Text in einzelne Tokens zu zerlegen und diese entsprechend verschiedener Kriterien zu bereinigen. Hierzu zählen das Entfernen von Stoppwörtern, den Ausschluss von Nicht-Alphanumeric-Zeichen und die mögliche Konvertierung segmentierter Wörter (z.B. "Fußball-Spiel" zu "Fußballspiel").

2. **Generierung von n-Grammen:** Die Methode `generate_ngrams` erstellt aus den Tokenlisten n-Gramme aus dem angegebenen Intervall unterschiedlicher Längen. Diese n-Gramme sind Kombinationen aufeinanderfolgender Tokens, die als eine Einheit betrachtet werden, um kontextuelle Informationen zu bewahren. Optional werden hierbei nur n-Gramme berücksichtigt, die mindestens ein Substantiv oder Nomen (großgeschriebenes Wort) enthalten. Die Umwandlung in Kleinbuchstaben erfolgt am Ende der n-Gram generierung. 

3. **Analysefunktion:** Die `analyzer`-Methode kombiniert die vorherigen Schritte, indem sie einen Text zunächst tokenisiert und dann n-Gramme aus den bereinigten Tokens erzeugt.

4. **CountVectorizer Integration:** Der `ArticleVectorizer` nutzt intern den `CountVectorizer`aus `sklearn.feature_extraction.text`, um die eigentliche Vektorisierung durchzuführen. Dieser wird mit den konfigurierten Parametern initialisiert, bekommt die `ArticleVectorizer.analyzer`-Methode und übernimmt die Aufgabe der Vektorisierung der vorverarbeiteten Artikel.

5. **Integration in die Pipeline:** Die `fit`- und `transform`-Methoden ermöglichen die Integration der Vektorisierungsfunktion in die Scikit-Learn-Pipeline. Während `fit` das Vokabular aus den Trainingsdaten lernt, transformiert `transform` die Artikeltexte in eine Häufigkeitsmatrix.

#### Helferfunktionen

Neben der Hauptfunktionalität verwendet der `ArticleVectorizer` zusätzliche Hilfsfunktionen wie `get_ngrams_with_capitalized`, `is_segmented_word` und `convert_segmented_word`, um spezifische Bereinigungs- und Transformationsschritte auf Tokens oder n-Grammen anzuwenden. Diese Funktionen tragen zur Präzision und Flexibilität des Vektorisierungsprozesses bei, indem sie spezifische sprachliche oder strukturelle Eigenschaften der Textdaten berücksichtigen.

### Matcher

#### TF-IDF und TfidfTransformer

TF-IDF ist eine statistische Methode, die dazu dient die Bedeutung eines Wortes in einem Dokument relativ zu einer Sammlung von Dokumenten (Korpus) zu bewerten.

- **Term Frequency (TF):** Maßzahl für die Häufigkeit eines Begriffs in einem Dokument.
- **Inverse Document Frequency (IDF):** Maß für die Wichtigkeit eines Begriffes in einem Korpus.

Das Produkt aus TF und IDF ergibt den TF-IDF-Wert eines Begriffs in einem Dokument. Ein hoher TF-IDF-Wert deutet darauf hin, dass der Begriff für das spezifische Dokument wichtig ist, aber in der gesamten Dokumentensammlung eher selten vorkommt.
Der `TfidfTransformer` aus der `scikit-learn` Bibliothek realisiert diese transformation.

#### Pipeline 

Die Häufigkeitsmatrix des `ArticleVectorizer` wird durch den `TfidfTransformer` in eine Tfidf-Matrix-Darstellung gebracht. Diese kann daraufhin verwendet werden um mit der Kosinus-Ähnlichkeit die Ähnlichkeit zwischen zwei Texten (bzw. zwischen Artikeln in leichter und normaler Sprache) zu berechnen. 
Das Artikel-Paar mit der größten Kosinus-Ähnlichkeit wird als Match identifiziert.

#### Ausblick

Der aktuelle Stand erlaubt die Definition eines Matchers, der das Preprocessing und die Vektorisierung durch den `ArticleVectorizer` und das Matching zwischen leichten und normalen Artikeln automatisiert und weitere artikelbezogene Matching-Kriterien und Parametereinstellungen umsetzt. 
Mögliche Matching-Kriterien und Parametereinstellungen:

- Berücksichtigung des Veröffentlichungsdatums
    - Maximale Differenz zwischen den Artikeln
    - time-decay als Bestrafungsterm
- Zeitrahmen des Korpus
    Einschränken des Zeitraums, aus dem Artikel stammen
- Vokabularbeschränkung (z.B. nur Artikel in leichter Sprache)
- Kombination aus Titel, Teaser, Beschreibung und Inhalt
- Berücksichtigung der Platzierung im Ranking
    - Auswahl aus den Score-Plätzen
    

Der zeitliche Rahmen des Projekts ermöglichte leider nicht die vollständige Entwicklung des Matchers. Zukünftig könnte der Matcher durch eine Ensemble-Methode verbessert werden. Es wäre sinnvoll, den `ArticleVectorizer` mit verschiedenen Parametern und Datensätzen auf die zu matchenden Artikel anzuwenden und durch ein Voting-System den "passenden" Artikel auszuwählen.

Ein lernbarer Zusammenhang zwischen den Parameterkonfigurationen und der Genauigkeit der einzelnen Matcher könnte hergestellt werden. Ein naiver Ansatz wäre Soft Voting, aber auch lineare Regression könnte als Evaluationsmethode dienen. Zum Trainieren eines solchen Modells könnte der bereits gematchte Datensatz der MDR-Artikel verwendet werden, da hier eine injektive Zuweisung besteht.

Zusammengefasst bietet dieser Ansatz eine flexible und anpassbare Methode zur Artikelverarbeitung und -matching, die durch weitere Verfeinerungen und die Implementierung zusätzlicher Kriterien noch präziser und leistungsfähiger gemacht werden kann.
