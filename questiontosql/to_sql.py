import torch
from transformers import BertForSequenceClassification, BertTokenizer
from questiontosql.transform_prediction_symp_dia import predict, transform_predictions

# **Intent-Model**
MODEL_PATH_INTENT = "DeliaMo/ner_intent"
intent_model = BertForSequenceClassification.from_pretrained(MODEL_PATH_INTENT)
intent_tokenizer = BertTokenizer.from_pretrained(MODEL_PATH_INTENT)

# **Label-mapping intent**
intent_label_map = {"get_symptoms": 0, "get_diagnose": 1}

# **Intent-Prediction**
def predict_intent(query):
    """
    Predict the intent of the input query using a pre-trained model.

    Args:
        query (str): The input query.

    Returns:
        str: The predicted intent.
    """
    inputs = intent_tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = intent_model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    intent = {v: k for k, v in intent_label_map.items()}[predicted_label]
    return intent

# **Entity Prediction**
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
    """
    Generate an SQL query based on the intent and extracted entities.

    Args:
        intent (str): The predicted intent.
        entities (List[str]): A list of extracted entities.

    Returns:
        str: The generated SQL query.
    """
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
        raise ValueError("Unknown intent: " + intent)
    return sql_query

# **Analyze Query (Intent + Entity Extraction)**
def analyze_query(user_input):
    """
    Analyzes the user input to predict the intent and extract symptom entities.

    Args:
        user_input (str): The input query from the user.

    Returns:
        dict: A dictionary containing the predicted intent and the list of extracted entities.
    """
    # Predict the intent using the existing function
    intent = predict_intent(user_input)

    # Extract entities using the existing function
    entities = extract_entities(user_input)

    return {
        "intent": intent,
        "entities": entities
    }

# **Analyze Query and Generate SQL**
def analyze_and_generate_sql(user_input):
    """
    Analyzes the user input to predict intent, extract entities, and generate an SQL query.

    Args:
        user_input (str): The input query from the user.

    Returns:
        dict: A dictionary containing the predicted intent, extracted entities, and the generated SQL query.
    """
    # Analyze the query (predict intent and extract entities)
    analysis_result = analyze_query(user_input)

    if not analysis_result["entities"]:
        return {"error": "No entities found in the query."}

    # Generate SQL query based on the intent and entities
    sql_query = generate_sql(analysis_result["intent"], analysis_result["entities"])

    return {
        "intent": analysis_result["intent"],
        "entities": analysis_result["entities"],
        "sql_query": sql_query
    }

# **Example usage:**
if __name__ == "__main__":
    user_input = input("Enter input: ")  
    result = analyze_and_generate_sql(user_input)

    # Accessing the results
    if "sql_query" in result:
        print("Intent:", result["intent"])  
        print("Entities:", result["entities"])  
        print(result["sql_query"]) 
    else:
        print(result["error"])  