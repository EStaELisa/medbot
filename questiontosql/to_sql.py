import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, BertForSequenceClassification, BertTokenizer

# **Intent-Model**
MODEL_PATH_INTENT = "./saved_model"
intent_model = BertForSequenceClassification.from_pretrained(MODEL_PATH_INTENT)
intent_tokenizer = BertTokenizer.from_pretrained(MODEL_PATH_INTENT)

# **NER-Model**
MODEL_PATH_NER = "./ner_model"
ner_model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH_NER)
ner_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH_NER)

# **Label-mappings**
intent_label_map = {"get_symptoms": 0, "get_diagnose": 1}
id_to_label_ner = {0: "O", 1: "B-ENTITY", 2: "I-ENTITY"}

# **Intent-Prediction**


def predict_intent(query):
    inputs = intent_tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = intent_model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    intent = {v: k for k, v in intent_label_map.items()}[predicted_label]
    return intent

# **Entity prediction**


def extract_entities(query):
    inputs = ner_tokenizer(query, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = ner_model(**inputs)
    predictions = outputs.logits.argmax(dim=2)
    tokens = ner_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    result = []
    current_entity = ""
    current_label = None

    for token, prediction in zip(tokens, predictions[0].numpy()):
        if token in ["[CLS]", "[SEP]", "[PAD]"]:
            continue
        label = id_to_label_ner[prediction]

        # Merge subtokens
        if token.startswith("##"):
            current_entity += token[2:]
        else:
            if current_entity:
                result.append((current_entity, current_label))
            current_entity = token
            current_label = label

    if current_entity:
        result.append((current_entity, current_label))

    # Filter out non-entities
    result = [(entity, label) for entity, label in result if label != "O"]
    return [entity for entity, _ in result]  # entity name

# **SQL-generation**


def generate_sql(intent, entities):
    if intent == "get_symptoms":
        sql_query = f"""
        SELECT Symptoms.name 
        FROM Symptoms
        JOIN Diagnoses ON Diagnoses.symptom_id = Symptoms.id
        WHERE Diagnoses.name IN ({', '.join(f"'{entity}'" for entity in entities)});
        """
    elif intent == "get_diagnose":
        sql_query = f"""
        SELECT Diagnoses.name 
        FROM Diagnoses
        JOIN Symptoms ON Symptoms.id = Diagnoses.symptom_id
        WHERE Symptoms.name IN ({', '.join(f"'{entity}'" for entity in entities)});
        """
    else:
        raise ValueError("Unbekannter Intent: " + intent)
    return sql_query


def handle_query(query):
    # get intent
    intent = predict_intent(query)
    if intent not in ["get_symptoms", "get_diagnose"]:
        return "Unbekannter Intent. Die Anfrage kann nicht verarbeitet werden."

    # get entities
    entities = extract_entities(query)
    if not entities:
        return "Keine Entitäten gefunden."

    # SQL generation
    sql_query = generate_sql(intent, entities)
    return sql_query
