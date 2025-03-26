# Datenvorverarbeitung und Symptomextraktion 

#### Beitrag von: Zeineb Souiai

Im Rahmen unseres Projekts war ich für den Entwurf und die Implementierung der Datenvorverarbeitungspipeline verantwortlich. Mein Ziel war es, aussagekräftige und strukturierte Symptominformationen aus unstrukturierten medizinischen Texten zu extrahieren.

Zunächst untersuchten wir den MIMIC-Datensatz, entschieden uns aber schließlich, ihn auszuschließen, da er keine direkten Zuordnungen von Symptomen zu Krankheiten lieferte, die für nachgelagerte Aufgaben des maschinellen Lernens verwendet werden könnten. Stattdessen konzentrierten wir uns auf den NHS-Datensatz, der für unseren Anwendungsfall geeignetere Inhalte bot.

## Prozess


### 1. Laden der Daten
CSV-Dateien von der NHS-Website wurden mit „pandas“ geladen. Diese enthielten Krankheitsnamen und unstrukturierte Symptombeschreibungen.

### 2. Benutzerdefinierte Stoppwort-Filterung
Ein benutzerdefinierter Satz von domänenspezifischen Stoppwörtern wurde verwendet, um irrelevante Wörter zu entfernen, die die Extraktion von Symptomen beeinträchtigen könnten. Dazu gehörten medizinische und generische Begriffe wie „einschließen“, „bekannt“, „Ursache“ usw.

### 3. Lemmatisierung
Der `WordNetLemmatizer` aus NLTK wurde verwendet, um Token auf ihre Stammform zu standardisieren (z.B. „swollen“ → „swelling“).

### 4. Symptom-Extraktion

- **Phrase Matching**: Verwendung einer kuratierten Liste von Symptomen und Phrasen (z. B. „chest pain“, „shortness of breath“) für den exakten Abgleich in vorverarbeitetem Text.
- **Regex-Matching**: Extraktion von Mustern nach Konstrukten wie „symptoms include“, „symptoms such as“ usw.
- **Erkennung von zusammengesetzten Wörtern**: Implementierte Logik zur Erkennung von bedeutungsvollen Mehrwortsätzen.

### 5. Filtern von nicht verwendbaren Einträgen
- Zeilen ohne aussagekräftige Symptome oder vage Begriffe wie „pain“ oder „flu“ allein wurden entfernt.
- Krankheiten wie „catarrh“ wurden mangels verwertbarer Symptomdaten ausgeschlossen.

### 6. Datenbereinigung und Ausgabe
- Die Symptome wurden dedupliziert und nach Krankheiten sortiert.
- Der endgültige Datensatz enthielt nur saubere, strukturierte Krankheits-Symptom-Einträge, die im CSV-Format gespeichert wurden.

## Skript-Iterationen
Während des gesamten Projekts habe ich mit mehreren Python-Skripten experimentiert, um die Extraktionslogik zu verfeinern und die Ergebnisse zu optimieren. Frühe Versionen wie nhs_prep.py und preprocessing.py wurden verwendet, um verschiedene Bibliotheken und Strategien für die Symptomzuordnung zu testen. Diese Versionen halfen mir, die Grenzen bestimmter Tools zu erkennen und die Logik iterativ zu verbessern. Die endgültige Arbeitsimplementierung wurde in prep_symptom_to_disease.py zusammengefasst, die den voll funktionsfähigen, optimierten Code enthält, der in der endgültigen Pipeline verwendet wird.



## Fazit
Die entwickelte Vorverarbeitungs- und Extraktionspipeline trug dazu bei, medizinischen Rohtext in saubere Symptom-Krankheit-Paare zu strukturieren, die für die Verwendung in der Datenbank unseres Chatbots und für nachgelagerte maschinelle Lernaufgaben geeignet sind. Der Prozess umfasste eine Kombination aus regelbasierten, musterbasierten und lexikalischen Techniken, die alle für die spezifischen Merkmale des NHS-Datensatzes optimiert wurden.

Dieser Schritt war entscheidend, um die Datenqualität zu verbessern und sicherzustellen, dass das weitere Modelltraining und die Abfrage auf zuverlässigen und relevanten Symptominformationen beruhen können.




