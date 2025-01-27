from transformers import pipeline

def explain_sql_query(sql_query):
    generator = pipeline('text-generation', model='t5-small')
    prompt = f"Explain this SQL query in natural language: {sql_query}"
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']