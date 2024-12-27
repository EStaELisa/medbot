import pytest
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# Load model and tokenizer
model = AutoModelForTokenClassification.from_pretrained("./ner_model")
tokenizer = AutoTokenizer.from_pretrained("./ner_model")
print("Model and tokenizer loaded successfully.")

# Label mapping
id_to_label = {0: "O", 1: "B-ENTITY", 2: "I-ENTITY"}

# Function to predict NER tags


def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    print("Tokens:", tokens)
    print("Predictions:", predictions[0].numpy())

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
    print("Result:", result)
    return result


# Test cases
@pytest.mark.parametrize(
    "test_text, expected",
    [
        ("The patient has fever and pneumonia.", [("fever", "B-ENTITY"), ("pneumonia", "B-ENTITY")]),
        ("Nausea and vomiting are common symptoms.", [("nausea", "B-ENTITY"), ("vomiting", "B-ENTITY")]),
        ("I suspect the patient has diabetes.", [("diabetes", "B-ENTITY")]),
        ("The person exhibits chills and fatigue.", [("chills", "B-ENTITY"), ("fatigue", "B-ENTITY")]),
        ("I have fever. What could be the diagnose?", [("fever", "B-ENTITY")]),
        ("What are the symptoms of pneumonia?", [("pneumonia", "B-ENTITY")])
    ],
)
def test_predict(test_text, expected):
    result = predict(test_text)
    # Normalize and compare results
    result_tokens = [(token.lower(), label) for token, label in result]
    expected_tokens = [(token.lower(), label) for token, label in expected]
    assert result_tokens == expected_tokens
