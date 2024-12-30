from typing import List, Tuple
from transformers import pipeline

class Span:
    """
    A class to represent a span (entity) in the text.

    Attributes:
    start (int): The starting position of the span in the text.
    end (int): The ending position of the span in the text.
    label (str): The label or type of the entity (e.g., PERSON, LOCATION).
    """
    def __init__(self, start: int, end: int, label: str):
        """
        Initialize a Span object.

        Args:
        start (int): The start position of the entity in the text.
        end (int): The end position of the entity in the text.
        label (str): The entity label (e.g., PERSON, LOCATION, etc.).
        """
        self.start = start
        self.end = end
        self.label = label

class NERAnonymizer:
    """
    A class for anonymizing text by replacing named entities with placeholders.

    Attributes:
    ner_model (transformers.Pipeline): The NER pipeline model for entity extraction.

    Methods:
    extract_entities(text: str) -> List[dict]: Extract entities from the text using NER.
    _merge_entities(entities) -> List[dict]: Merge overlapping or split entities into full spans.
    anonymize(text: str) -> str: Anonymize the text by replacing identified entities with placeholders.
    _get_replacement(entity_type: str) -> str: Get the placeholder for the entity based on its type.
    """
    def __init__(self, model_path: str) -> None:
        """
        Initialize the NERAnonymizer with a fine-tuned model for entity recognition.

        Args:
        model_path (str): Path to the fine-tuned NER model directory.
        """
        self.ner_model = pipeline("ner", model=model_path, tokenizer=model_path)

    def extract_entities(self, text: str) -> List[dict]:
        """
        Extract entities from the text using the NER pipeline.

        Args:
        text (str): The input text to extract entities from.

        Returns:
        List[dict]: A list of dictionaries, each containing entity information
                    like its start and end positions, and entity type.
        """
        # Use the NER pipeline to get the predictions
        ner_results = self.ner_model(text)
        return ner_results

    def _merge_entities(self, entities) -> List[dict]:
        """
        Merge subwords and overlapping entities into single spans.

        Args:
        entities (List[dict]): A list of entities as returned by the NER pipeline.

        Returns:
        List[dict]: A list of merged entities, where each entity is a dictionary
                    containing its start, end, and text representation.
        """
        merged_entities = []
        current_entity = None

        for token in entities:
            if token['entity'] == '0':  # Skip non-entity tokens
                continue

            entity_type = token['entity'].split('-')[-1]  # Strip B- or I- prefix

            if not current_entity or token['entity'].startswith('B-') or current_entity['entity'] != entity_type:
                # Start a new entity span
                if current_entity:
                    merged_entities.append(current_entity)
                current_entity = {
                    'entity': entity_type,
                    'start': token['start'],
                    'end': token['end'],
                    'text': token['word'].replace("##", "")
                }
            else:
                # Continue the current entity span
                current_entity['end'] = token['end']
                current_entity['text'] += token['word'].replace("##", "")

        # Add the last entity
        if current_entity:
            merged_entities.append(current_entity)

        return merged_entities

    def anonymize(self, text: str) -> str:
        """
        Anonymize the text by replacing identified entities with placeholders.

        Args:
        text (str): The input text to anonymize.

        Returns:
        str: The anonymized text with entities replaced by placeholders like
             <PERSON>, <LOCATION>, <ORG>, <EMAIL>, <PHONE>.
        """
        entities = self.extract_entities(text)
        merged_entities = self._merge_entities(entities)

        offset = 0
        for entity in merged_entities:
            start, end = entity['start'] + offset, entity['end'] + offset
            replacement = self._get_replacement(entity['entity'])

            # Replace the text and update offset
            text = text[:start] + replacement + text[end:]
            offset += len(replacement) - (end - start)

        return text

    def _get_replacement(self, entity_type: str) -> str:
        """
        Get the placeholder replacement text based on the entity type.

        Args:
        entity_type (str): The type of entity (e.g., PER, GPE, ORG).

        Returns:
        str: The placeholder string that will replace the entity in the text.
        """
        replacements = {
            'PER': '<PERSON>',
            'GPE': '<LOCATION>',
            'ORG': '<ORG>',
            'EMAIL': '<EMAIL>',
            'PHONE': '<PHONE>',
        }
        return replacements.get(entity_type, '<ENTITY>')

if __name__ == "__main__":
    # Example text
    text = "John Doe lives in New York and works at Google. You can reach them via johndoe@google.com or +4911112239."

    # Path to your fine-tuned model
    model_path = "data/ner_finetuned_model"

    # Instantiate and use the anonymizer
    anonymizer = NERAnonymizer(model_path)
    anonymized_text = anonymizer.anonymize(text)

    print("Original text:", text)
    print("Anonymized text:", anonymized_text)
