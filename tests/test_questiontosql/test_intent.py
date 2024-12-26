import torch
from transformers import BertForSequenceClassification, BertTokenizer

# Load the saved model and tokenizer
MODEL_PATH = "./saved_model"
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)

# Define label mapping
label_map = {"get_symptoms": 0, "get_diagnose": 1}

# Function to predict intent


def predict_intent(query, model, tokenizer, label_map):
    # Tokenize the input query
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=128)

    # Perform inference
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()

    # Convert label index back to intent
    intent = {v: k for k, v in label_map.items()}[predicted_label]
    return intent

# Test cases


def run_tests():
    test_queries = [
        "What are the symptoms of pneumonia?",
        "I have fever and chills, what could it be?",
        "What might cause shortness of breath and nausea?",
        "Tell me the symptoms of influenza.",
        "I am experiencing chills and a headache, what might it mean?",
        "My patient suffers from headache, could you provide me with a diagnose?",
        "What diagnose can be made for a patient with fever and cough?",
        "I was diagnosed with Huntingtons disease, what can I expect?",
        "I have Huntingtons disease, what can I expect?",
        "May patint has lung cancer what will he exprience?",
    ]

    for query in test_queries:
        intent = predict_intent(query, model, tokenizer, label_map)
        print(f"Query: {query}")
        print(f"Predicted Intent: {intent}\n")


if __name__ == "__main__":
    print("Running tests for intent classification model...\n")
    run_tests()
