import re
from typing import List, Tuple
from transformers import pipeline
import pandas as pd
from faker import Faker

# Beispiel für die Span-Klasse
class Span:
    def __init__(self, start: int, end: int, label: str):
        self.start = start
        self.end = end
        self.label = label

# Abstrakte Klasse für die Anonymisierung
class Anonymizer:
    def __init__(self) -> None:
        pass

    def anonymize(self, span: Span, text: str) -> Tuple[Span, str]:
        """Methode zur Anonymisierung eines Textbereichs."""
        raise NotImplementedError

# NER-basierte Anonymisierung mit einem Transformer-Modell (BERT)
class NERAnonymizer(Anonymizer):
    def __init__(self) -> None:
        super().__init__()
        # Vortrainiertes NER-Modell laden
        self.ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def anonymize(self, span: Span, text: str) -> Tuple[Span, str]:
        # Entitäten mit dem NER-Modell extrahieren
        entities = self.extract_entities(text)

        for entity in entities:
            entity_type = entity['entity']
            entity_text = entity['word']
            start = entity['start']
            end = entity['end']

            # Anonymisierungsmaßnahmen je nach Entitätstyp anwenden
            if entity_type == 'PER':
                new_text = self._replacePER(entity_text)
            elif entity_type == 'LOC':
                new_text = self._replaceLOC(entity_text)
            elif entity_type == 'DATE':
                new_text = self._replaceDATE(entity_text)
            else:
                new_text = self._replaceDefault(entity_text)

            # Ersetze die identifizierte Entität im Text
            text = text[:start] + new_text + text[end:]

        return (span, text)

    def extract_entities(self, text: str):
        """Extrahiert benannte Entitäten aus dem Text mithilfe des NER-Modells."""
        return self.ner_model(text)

    def _replacePER(self, text: str) -> str:
        """Ersetzt Person-Entitäten mit <PERSON>."""
        return "<PERSON>"

    def _replaceLOC(self, text: str) -> str:
        """Ersetzt Orts-Entitäten mit <LOCATION>."""
        return "<LOCATION>"

    def _replaceDATE(self, text: str) -> str:
        """Ersetzt Datums-Entitäten mit <DATE>."""
        return "<DATE>"

    def _replaceDefault(self, text: str) -> str:
        """Standardersatz, wenn keine spezifische Kategorie erkannt wird."""
        return "<ENTITY>"

# Funktion zur Anonymisierung von Textbereichen
def anonymizeSpans(anonymizer: NERAnonymizer, spans: List[Span], text: str) -> Tuple[List[Span], str]:
    new_spans = []
    offset = 0
    for span in spans:
        span.start += offset
        span.end += offset
        new_span, new_text = anonymizer.anonymize(span, text)
        text = new_text
        offset += new_span.end - span.end
        new_spans.append(new_span)
    return (new_spans, text)

# Beispielnutzung
if __name__ == "__main__":
    # Beispieltext
    text = "John Doe lebt in New York und arbeitet am 01.10.2024."

    # Beispielhafte Textbereiche (nur als Platzhalter)
    spans = [Span(0, 8, 'PER'), Span(19, 27, 'LOC'), Span(43, 53, 'DATE')]

    # NERAnonymizer-Instanz erstellen
    anonymizer = NERAnonymizer()

    # Den Text anonymisieren
    new_spans, anonymized_text = anonymizeSpans(anonymizer, spans, text)
    print("Originaltext:", text)
    print("Anonymisierter Text:", anonymized_text)
