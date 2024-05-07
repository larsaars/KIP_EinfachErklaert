## Einleitung

Die Umsetzung eines Projekts ist oft von verschiedenen Herausforderungen geprägt, die von technischen Aspekten bis hin zu organisatorischen Belangen reichen. In diesem Projektbericht werden sowohl technische als auch organisatorische Herausforderungen beleuchtet, die während der Implementierung bewältigt wurden. Besonderes Augenmerk liegt dabei auf der Integration neuer Teammitglieder, der remote Durchführung von Meetings sowie der Kommunikation mit Nachrichtenquellen wie Deutschlandfunk und MDR. Zudem wird die Datenstruktur für die Speicherung und das Scraping erläutert sowie ein Ausblick auf den Matching-Prozess gegeben, der für die Nutzung des aufgebauten Datensatzes von zentraler Bedeutung ist. Zuletzt geben wir einen kleinen Ausblick auf den weiteren Verlauf des Projekts.
## Aktueller Stand 
### Kommunikation mit Nachrichtenquellen

Die Kommunikation mit den Nachrichtenquellen gestaltete sich als ein Bestandteil unseres Projekts. Wir wandten uns an Deutschlandfunk und MDR, um Zugang zu ihren Nachrichteninhalten zu erhalten, da wir bereits bei Deutschlandfunk auf Schwierigkeiten beim Scrapen historischer Daten gestoßen sind und es als eine alternative Möglichkeit gesehen haben, dort direkt anzufragen. Es ist hier deutlich schwerer an die Daten zu kommen, da einerseits viel mehr publiziert wird im Vergleich zu Nachrichtenleicht und es keine einfach abrufbare API gibt. Über verschiedene Kanäle wie E-Mail, Instagram, TikTok und LinkedIn versuchten wir, Kontakt herzustellen. Nach diesen mehreren Versuchen erhielten wir zuerst eine Antwort auf TikTok, dass es an das Team von Nachrichtenleicht weitergeleitet wurde. Einen Tag später kam dann eine Antwort von Herrn Bertolaso, einem leitenden Nachrichtenredakteur bei Deutschlandfunk. Er leitete unsere Anfrage weiter an Frau Gnad, und wir befinden uns derzeit in der Warteposition, in der Hoffnung auf weitere Unterstützung. Nach einem Telefonat mit Frau Gnad stellte sich heraus, dass noch die Möglichkeit besteht tagesaktuelle Daten aus den Instagram Captions von Nachrichten Leicht zu scrapen. Desweiteren hat sie uns mit dem Archiv in Verbindung gesetzt. Die Mitarbeitenden werden sich da in den nächsten Tagen bei uns melden, ob uns geholfen werden kann. Da MDR als Quelle erst letzte Woche dazu kam, ist hier leider noch kein Erfolgserlebnis zu verzeichnen, da bis jetzt nur Antworten kamen, dass es an die zuständige Redaktion weitergeleitet wurde.
Wir erwogen auch eine Zusammenarbeit mit der anderen Gruppe, die das gleiche Projekt durchführt, nachdem sich in einem Gespräch mit Prof. Baumann herausstellte, dass es sinnvoll sein könnte, sich beim Scrapen die Arbeit zu teilen. Jedoch wurde unsere Anfrage abgelehnt, da die andere Gruppe befürchtete, dass eine Auslagerung des Webscrapings zu einem Verlust in der Bewertung führen könnte, da dies ja auch Teil der Aufgabenstellung ist und auch einen gewissen Teil des Arbeitsaufwandes darstellt.


### Über den KI-Server

Die Datenspeicherung und das Scraping (später auch das Matching der Artikel) finden über den KI-Server der OTH statt. Dies war von Anfang an die Idee, da dieser eine hohe Rechenleistung bietet und somit das Scraping und unsere kommenden Schritte (siehe [Ausblick](#ausblick)) schneller und effizienter gestaltet. Seit kurzem existiert auich die Ordnerstruktur und die Daten werden automatisiert gespeichert. 

Mithilfe eines Cronjobs werden die Scraping-Skripte regelmäßig ausgeführt, um die neuesten Artikel zu speichern. Wie bereits erwähnt, veröffentlicht Nachrichtenleicht wöchentlich neue Artikel und Deutschlandfunk, sowie MDR, täglich. Demnach wird es zwei Skripte geben. Eines, das einmal am Tag ausgeführt wird und die neuen Artikel von Nachrichtenleicht speichert und eines, das alle zwei Stunden ausgeführt wird und die neuen Artikel von Deutschlandfunk und MDR speichert oder aktualisiert. Sollten wir mit diesen noch experimentellen Zeiträumen für die Ausführung der Skripte auf Probleme stoßen, werden wir diese gerade am Anfang der Scraping-Phase natürlich auch noch anpassen.

## Ausblick

Nachdem wir den Datensatz aufgebaut haben, wird der nächste spannende Schritt in unserem Projekt der Matching-Prozess sein. Dieser Prozess ist entscheidend, da der aufgebaute Datensatz hiermit erst wirklich brauchbar gemacht wird. Wir planen, fortschrittliche Techniken der natürlichen Sprachverarbeitung (NLP) und des maschinellen Lernens zu nutzen, um eine hohe Genauigkeit und Effizienz bei der Zuordnung von Artikelpaaren zu erreichen.

Wir werden uns auf mehrere verschiedene Ansätze konzentrieren, um die besten Ergebnisse zu erzielen. Prinzipiell wird der Matcher so arbeiten, dass zu einem Artikel der leichten Nachrichten eine Zuordnung zu einem Artikel der schweren Nachrichten erfolgt. Wir haben deutlich weniger Artikel in leichter Sprache und es ist fast sicher, dass zu jedem dieser Artikel einer in schwerer Sprache in unserem Datensatz existiert, demnach macht es Sinn, auf diese Art und Weise zu matchen. Hierbei müssen wir uns tatsächlich nur auf die Artikel von `Deutschlandfunk` und `Nachrichtenleicht` konzentrieren, da der `MDR` auf ihrer Webseite jeweils den schweren Artikel verlinken und damit das matching schon gegeben ist. 

#### Base Matcher (Felix)

### Matching

Wir haben einige grundlegende Recherchen zu verschiedenen Matching-Methoden durchgeführt, die wir in den nächsten Wochen weiter vertiefen möchten. Einzelne Ideen, die wir ausbauen und erweitern wollen, sind:

#### Hugging Face

Ein hilfreiches Element dabei ist die Plattform Hugging Face, die eine große Bibliothek von Pre-Training-Models für unter anderem NLP-Aufgaben bietet. Diese Modelle sind nicht nur leistungsstark, sondern auch anpassungsfähig, was uns die Möglichkeit gibt, sie auf unsere spezifischen Anforderungen zuzuschneiden oder Teile davon als Inspiration zu verwenden. Es gibt dort Modelle zu den verschiedensten Arten der Textanalyse, womit durch einiges Experimentieren mit den Modellen viel gewonnen werden kann.

#### Named Entity Recognition

Ein vielversprechender Ansatz, den wir in Betracht ziehen, ist die Named Entity Recognition (NER). NER ist eine Technik, die wir bei unseren Recherchen gefunden haben und nutzen möchten. Diese ermöglicht es uns, aus Texten spezifische Informationen wie Namen von Personen, Organisationen oder Orte zu extrahieren. Diese Identifikation und Klassifikation von Entitäten ist für das Matching von entscheidender Bedeutung, da sie es uns erlaubt, bei gleichen Ergebnissen möglichen Textpaares zu erstellen. Auf Huggingface kann man einige Modelle direkt in der Webseite testen, hierbei konnten wir bei kurzen Tests schon vielversprechende Ergebnisse erzielen. Wir planen, die NER-Modelle so zu trainieren, dass diese speziell auf unseren Datensatz zugeschnitten sind, um die bestmögliche Leistung zu erzielen.

#### BERT

Wir planen auch, das leistungsstarke Modell BERT (Bidirectional Encoder Representations from Transformers) zu nutzen, um die Themenähnlichkeit zwischen zwei Texten zu ermitteln. BERT basiert auf einer speziellen Variante der Transformer-Architektur und ermöglicht eine Analyse von Texten. Dies erlaubt eine präzisere Erfassung des Kontexts eines Wortes oder einer Wortgruppe in einem Satz. Im Hinblick auf die Semantik können wir damit Übereinstimmungen feststellen und herausfinden, ob zwei Texte das gleiche Thema behandeln.

Allgemein könnte es hilfreich sein, einen Datensatz mit gelabelten Beispielen zu haben, um das Modell zu trainieren und zu validieren. Diesen werden wir voraussichtlich in kleinem Maße händisch erstellen und je nach Bedarf erweitern. Im Idealfall wird uns dieser Ansatz ermöglichen, eine präzise und effiziente Methode zur Themenidentifikation in Texten zu implementieren.

