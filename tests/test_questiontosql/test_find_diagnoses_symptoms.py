import pytest
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# load model and tokenizer
model = AutoModelForTokenClassification.from_pretrained("./ner_model")
tokenizer = AutoTokenizer.from_pretrained("./ner_model")

# label mapping
id_to_label = {0: "O", 1: "B-SYMPTOM", 2: "I-SYMPTOM", 3: "B-DIAGNOSE", 4: "I-DIAGNOSE"}

# function to predict NER tags


def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    result = []
    for token, prediction in zip(tokens, predictions[0].numpy()):
        if id_to_label[prediction] != "O":
            result.append((token, id_to_label[prediction]))
    return result


# test cases
@pytest.mark.parametrize(
    "test_text, expected",
    [
        ("The patient has fever and pneumonia.", [("fever", "B-SYMPTOM"), ("pneumonia", "B-DIAGNOSE")]),
        ("Nausea and vomiting are common symptoms.", [("Nausea", "B-SYMPTOM"), ("vomiting", "B-SYMPTOM")]),
        ("I suspect the patient has diabetes.", [("diabetes", "B-DIAGNOSE")]),
        ("The person exhibits chills and fatigue.", [("chills", "B-SYMPTOM"), ("fatigue", "B-SYMPTOM")]),
    ],
)
def test_predict(test_text, expected):
    result = predict(test_text)
    # remove special token character
    result_tokens = [(token.replace("▁", ""), label) for token, label in result]
    assert result_tokens == expected
