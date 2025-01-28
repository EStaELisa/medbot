from transformers import pipeline

def explain_sql_query(sql_query):
    # Verwende ein leistungsstarkes vortrainiertes Modell wie Flan-T5
    generator = pipeline("text2text-generation", model="google/flan-t5-large")

    # Eingabe-Prompt mit Kontext für SQL-Erklärung
    prompt = (
        "Explain the following SQL query in clear, natural language. "
        "Break it into parts (table, columns, filters) and describe what it does:\n\n"
        f"SQL query: {sql_query}"
    )

    # Generiere Erklärung
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']