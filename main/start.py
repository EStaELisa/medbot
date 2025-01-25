from fastapi_backend.app.questiontosql import predict_intent, extract_entities, generate_sql


def start(query):

    # ANONYMIZATION HERE
    query_anon = query

    # build sql query
    intent = predict_intent(query_anon)
    entities = extract_entities(query_anon)
    sql_query = generate_sql(intent, entities)

    # get result from database

    # generate text response
    if intent == "get_symptoms":
        response = f"The symptoms for {', '.join(entities)} are: "
    elif intent == "get_diagnose":
        response = f"Possible diagnoses for the symptoms {', '.join(entities)} are: "

    return response
