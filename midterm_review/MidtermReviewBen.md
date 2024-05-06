## Einleitung

## Aktueller Stand 
### Kommunikation mit Nachrichtenquellen

Die Kommunikation mit den Nachrichtenquellen gestaltete sich als ein Bestandteil unseres Projekts. Wir wandten uns an Deutschlandfunk und MDR, um Zugang zu ihren Nachrichteninhalten zu erhalten, da wir bereits bei Deutschlandfunk auf Schwierigkeiten beim Scrapen historischer Daten gestoßen sind und es als eine alternative Möglichkeit gesehen haben dort direkt anzufragen. Es ist hier deutlich schwerer an die Daten zu kommen, da einerseits viel mehr publiziert wird im Vergleich zu Nachrichtenleicht und es keine einfach abrufbare API gibt. Über verschiedene Kanäle wie E-Mail, Instagram, Tiktok und LinkedIn versuchten wir, Kontakt herzustellen. Nach diesen mehreren Versuchen erhielten wir zuerst eine Antwort auf Tiktok, dass es an das Team von Nachrichtenleicht weitergeleitet wurde. Einen Tag später kam dann eine Antwort von Herrn Bertolaso, einem leitenden Nachrichtenredakteur bei Deutschlandfunk. Er leitete unsere Anfrage weiter an Frau Gnad, und wir befinden uns derzeit in der Warteposition, in der Hoffnung auf weitere Unterstützung. Hierbei ist für diese Woche ein Telefonat angesetzt, in dem wir unser Projekt nochmal genauer vorstellen können und konkret besprechen, ob und in welcher Art uns Daten zur Verfügung gestellt werden können. Da MDR als Quelle erst letzte Woche dazu kam, ist hier leider noch kein Erfolgserlebnis zu verzeichnen, da bis jetzt keine Antwort auf einem der Kanäle erfolgte. 

Wir erwogen auch eine Zusammenarbeit mit der anderen Gruppe, die das gleiche Projekt durchführt, nachdem sich in einem Gespräch mit Prof. Baumann herausstellte, dass es sinnvoll sein könnte sich beim Scrapen die Arbeit zu teilen. Jedoch wurde unsere Anfrage abgelehnt, da die andere Gruppe befürchtete, dass eine Auslagerung des Webscrapings zu einem Verlust in der Bewertung führen könnte, da dies ja auch Teil der Aufgabenstellung ist und auch einen gewissen Teil des Arbeitsaufwandes darstellt.


### Über den KI-Server

Die Datenspeicherung und das Scraping (später auch das Matching der Artikel) werden über den KI-Server der OTH stattfinden. Dies war von Anfang an die Idee, da dieser eine hohe Rechenleistung bietet und somit das Scraping und unsere kommenden Schritte (siehe [Ausblick](#ausblick)) schneller und effizienter gestaltet werden kann. Zeitnah werden wir, in einem eigens dafür vorgesehenen Directory die bereits erwähnte Speicherstruktur anlegen.

Mithilfe eines Cronjobs werden wir die Scraping-Skripte regelmäßig ausführen, um die neuesten Artikel zu speichern. Wie bereits erwähnt, veröffentlicht Nachrichtenleicht wöchentlich neue Artikel und Deutschlandfunk, sowie MDR, täglich. Demnach wird es zwei Skripte geben. Eines, das mehrmals wöchentlich ausgeführt wird und die neuen Artikel von Nachrichtenleicht speichert und eines, das zweimal täglich ausgeführt wird und die neuen Artikel von Deutschlandfunk und MDR speichert oder aktualisiert. Sollten wir mit diesen experimentellen Zeiträumen für die Ausführung der Skripte auf Probleme stoßen, werden wir diese gerade am Anfang der Scraping-Phase natürlich auch noch anpassen.

## Ausblick

Nachdem wir den Datensatz aufgebaut haben, wird der nächste spannende Schritt in unserem Projekt der Matching-Prozess sein. Dieser Prozess ist entscheidend, da der aufgebaute Datensatz hiermit erst wirklich brauchbar gemacht wird. Wir planen, fortschrittliche Techniken der natürlichen Sprachverarbeitung (NLP) und des maschinellen Lernens zu nutzen, um eine hohe Genauigkeit und Effizienz bei der Zuordnung von Artikelpaaren zu erreichen.

Wir werden uns auf mehrere verschiedene Ansätze konzentrieren, um die besten Ergebnisse zu erzielen. Prinzipiell wird der Matcher so arbeiten, dass zu einem Artikel der leichten Nachrichten eine Zuordnung zu einem Artikel der schweren Nachrichten erfolgt. Wir haben deutlich weniger Artikel in leichter Sprache und es ist fast sicher, dass zu jedem dieser Artikel einer in schwerer Sprache in unserem Datensatz existiert, demnach macht es Sinn auf diese Art und Weise zu matchen. Hierbei müssen wir uns tatsächlich nur auf die Artikel von `Deutschlandfunk` und `Nachrichtenleicht` konzentrieren, da der `MDR` auf ihrer Webseite jeweils den schweren Artikel verlinken und damit das matching schon gegeben ist. 

#### Base Matcher (Felix)

### Matching

Wir haben einige grundlegende Recherchen zu verschiedenen Matching-Methoden durchgeführt, die wir in den nächsten Wochen weiter vertiefen möchten. Einzelne Ideen, die wir ausbauen und erweitern wollen, sind:

#### Huggingface

Ein hilfreiches Element dabei könnte die Plattform Hugging Face werden, die eine große Bibliothek von Pre-Training-Models für unter anderem NLP-Aufgaben bietet. Diese Modelle sind nicht nur leistungsstark, sondern auch anpassungsfähig, was uns die Möglichkeit gibt, sie auf unsere spezifischen Anforderungen zuzuschneiden oder Teile davon als Inspiration zu verwenden. Durch die Verwendung von Hugging Face können wir vorhandene Modelle verbessern und anpassen, um die bestmöglichen Ergebnisse für unser Matching-Problem zu erzielen.

#### Named Entity Recognition

Ein vielversprechender Ansatz, den wir in Betracht ziehen, ist die Named Entity Recognition (NER) sein. NER ist eine Technik, die wir bei unseren Recherchen gefunden haben und nutzen möchten. Diese ermöglicht es uns, aus Texten spezifische Informationen wie Namen von Personen, Organisationen oder Orte zu extrahieren. Diese präzise Identifikation und Klassifikation von Entitäten ist für das Matching von entscheidender Bedeutung, da sie es uns erlaubt, die Relevanz und Genauigkeit der Textpaare zu bewerten. Wir planen, NER-Modelle zu trainieren, die speziell auf unseren Datensatz zugeschnitten sind, um die bestmögliche Leistung zu erzielen.

#### BERT