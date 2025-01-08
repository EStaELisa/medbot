from transformers import pipeline

def output_sql(sql_query):
    # print sql
    print("Generated SQL query:")
    print(sql_query)

    # print explanation
    explanation = explain_sql_query(sql_query)
    print(explanation)

def explain_sql_query(sql_query):
    # t5-small modell to explain
    generator = pipeline('text-generation', model='t5-small')

    # generate response
    prompt = f"Explain this SQL query in natural language: {sql_query}"
    response = generator(prompt, max_length=150, num_return_sequences=1)

    return response[0]['generated_text']
