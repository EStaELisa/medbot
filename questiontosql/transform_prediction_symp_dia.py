from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# Load model and tokenizer
model = AutoModelForTokenClassification.from_pretrained("./ner_model")
tokenizer = AutoTokenizer.from_pretrained("./ner_model")
print("Model and tokenizer loaded successfully.")

# Label mapping
id_to_label = {0: "O", 1: "B-ENTITY", 2: "I-ENTITY"}


def predict(text):
    """
    Predicts named entities in the input text using the NER model.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    result = []
    current_entity = ""
    current_label = None

    for token, prediction in zip(tokens, predictions[0].numpy()):
        if token in ["[CLS]", "[SEP]", "[PAD]"]:
            continue

        label = id_to_label[prediction]

        # Merge subtokens
        if token.startswith("##"):
            current_entity += token[2:]
        else:
            if current_entity:
                result.append((current_entity, current_label))
            current_entity = token
            current_label = label

    # Append last entity
    if current_entity:
        result.append((current_entity, current_label))

    # Filter out non-entities
    result = [(entity, label) for entity, label in result if label != "O"]
    return result


def transform_predictions(predictions):
    """
    Transforms the raw predictions into a structured format for easier use.

    Args:
        predictions (list): List of tuples from the predict function [(entity, label), ...]

    Returns:
        dict: A structured dictionary with entities grouped by type.
    """
    structured_data = {"entities": []}

    for entity, label in predictions:
        structured_data["entities"].append({"text": entity, "type": label})

    return structured_data
