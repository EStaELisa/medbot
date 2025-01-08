import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, BertForSequenceClassification, BertTokenizer

from XAI import anonymization_explanation, sql_explanation
from questiontosql.transform_prediction_symp_dia import predict, transform_predictions

# **Intent-Model**
MODEL_PATH_INTENT = "DeliaMo/ner_intent"
intent_model = BertForSequenceClassification.from_pretrained(MODEL_PATH_INTENT)
intent_tokenizer = BertTokenizer.from_pretrained(MODEL_PATH_INTENT)

# **Label-mapping intent**
intent_label_map = {"get_symptoms": 0, "get_diagnose": 1}

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
    """
    Extract entities from a query using NER predictions.

    Args:
        query (str): The input query.

    Returns:
        List[str]: A list of extracted entities.
    """
    predictions = predict(query)
    structured_data = transform_predictions(predictions)
    return [entity["text"] for entity in structured_data["entities"]]


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
    """
    Handles a query by predicting intent, extracting entities, and generating SQL.

    Args:
        query (str): The input query.

    Returns:
        str: Generated SQL query or an error message.
    """
    # Predict intent
    intent = predict_intent(query)
    if intent not in ["get_symptoms", "get_diagnose"]:
        return "Unknown intent. Query cannot be precessed."

    # Extract entities
    entities = extract_entities(query)
    if not entities:
        return "No entity found."

    # Generate SQL
    sql_query = generate_sql(intent, entities)
    sql_explanation.output_sql(sql_query)
    return sql_query
