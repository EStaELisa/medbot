from transformers import BertForSequenceClassification, BertTokenizer
import uuid
from fastapi_backend.app.XAI import intent_explanation, anonymization_explanation

def explain(text, anon_text, entities, sql_query):
    """
    Generates an explanation for a given input text by analyzing anonymization, intent classification and SQL query generation.

    Args:
        text (str): The original user input.
        anon_text (str): The anonymized version of the user input.
        entities (list): A list of extracted entities with confidence scores.
        sql_query (str): The SQL query based on the input text.

    Returns:
        str: A unique identifier for the generated explanation file.

    The function loads a fine-tuned BERT model for intent classification, applies anonymization explanations, and generates
    an explanation for the intent classification using LIME. It then creates a combined explanation file containgin all
    relevant components.
    """
    model_path = "DeliaMo/ner_intent"
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    anonymization_explanation.print_anon_text(anon_text)
    anonymization_explanation.explain_anonymization(entities)

    wrapper = intent_explanation.ModelWrapper(model, tokenizer, {"get_symptoms": 0, "get_diagnose": 1})

    explanationid = uuid.uuid4()
    explanation_path = "fastapi_backend/app/static/explanations/" + str(explanationid) + ".html"
    intent_html = intent_explanation.lime_explanation(wrapper, anon_text)

    create_combined_explanation(text, anon_text, entities, intent_html, explanation_path, sql_query)
    return str(explanationid)

def create_combined_explanation(text, anon_text, entities, intent_html, path, sql_query):
    """
    Generate a single HTML file with explanations for anonymization and LIME explanations.

    Args:
    - model_wrapper: The model wrapper with predict_proba method.
    - text: The original input text.
    - anonymized_text: The text after anonymization.
    - entities: List of entities with confidence scores.
    """

    safe_sql_query = sql_query.replace('<', '&lt;').replace('>', '&gt;')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device, initial-scale=1.0">
        <title>Explanations</title>
        <style>
            body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 5px;
            padding: 5px;
            background-color: #f9f9f9;
            color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1, h2 {{
                color: #2c3e50;
            }}
            .code {{
                background: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow: auto;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Explanation</h1>
            <p><strong>Input Prompt</strong></p>
            <div class="code">{text}</div>
            <h2>Anonymization</h2>
            <p><strong>Anonymized Text:</strong></p>
            <div class="code">{anon_text.replace('<', '&lt;').replace('>', '&gt;')}</div>
            <p><strong>Entities:</strong></p>
            <ul>
    """
    for entity in entities:
        confidence = entity['confidence']
        if confidence > 0.9:
            explanation = "The model is very confident."
        elif confidence > 0.7:
            explanation = "The model is somewhat confident, but there is some uncertainty."
        else:
            explanation = "The model is not very confident; this could be a random prediction."

        html_content += f"<li>Entity: {entity['text']} | Type: {entity['entity']} | Confidence: {entity['confidence']:.2f} | {explanation}</li>"
    html_content += """
            </ul>

            <h2>Intent Model</h2>
    """
    html_content += f"<div>{intent_html}</div>"
    html_content += f"""
    <h2>SQL Query</h2>
            <p><strong>Generated SQL Query:</strong></p>
            <div class="code">{safe_sql_query}</div>
    </body>
    </html>
    """

    with open(path, "w") as file:
        file.write(html_content)