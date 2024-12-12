

# Eingabedaten einlesen

# Beispieltext
text = "John Doe lives in Berlin and works for OpenAI. His phone number is 123-456-7890."

# Model laden

from transformers import pipeline

# NER-Pipeline mit dem Modell laden
ner_pipeline = pipeline(
    "ner",
    model="xlm-roberta-large-finetuned-conll03-english",
    tokenizer="xlm-roberta-large-finetuned-conll03-english",
    grouped_entities=True  # Gruppiert zusammenhängende Entitäten
)

# TrueCaser - Groß/Kleinschreibung wird normalisiert

# Sensible Daten identifizieren

# Anonymisierung

# Named Entity Recognition ausführen
entities = ner_pipeline(text)

# Ergebnis speichern

# Ergebnisse anzeigen
for entity in entities:
    print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.2f}")

