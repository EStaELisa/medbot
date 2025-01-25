import os
import psycopg2
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.AnonymizationPipeline import anonymize
from app.questiontosql import to_sql
from app.XAI import explainer

db_host = os.getenv("PGHOST", "db")
db_name = os.getenv("PGDATABASE", "postgres")
db_user = os.getenv("PGUSER", "postgres")
db_password = os.getenv("PGPASSWORD", "postgres")
db_port = os.getenv("PGPORT", "5432")


def connect_and_query(generated_query):
    # Connection parameters (replace these with your actual database credentials)
    db_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port,
    }

    try:
        # Establish the connection
        conn = psycopg2.connect(**db_params)

        # Create a cursor object
        cursor = conn.cursor()

        # Write your SQL query
        query = generated_query

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()  # Fetch all rows returned by the query

        # Print the results (you can process them further if needed)
        for row in results:
            print(row)

    except Exception as e:
        print(f"Error: {e}")


    finally:
        # Close the cursor and the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return results

def generate_result(intent, entities, generated_query):
    db_answer = connect_and_query(generated_query)
    clean_response = stringify_database_response(db_answer)
    if intent == "get_symptoms":
        response = f"The symptoms for {', '.join(entities)} are: {clean_response}"
    elif intent == "get_diagnose":
        response = f"Possible diagnoses for the symptoms {', '.join(entities)} are: {clean_response}"
    return response

class Message(BaseModel):
    text: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins (adjust as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

def stringify_database_response(database_array):
    clean_response = ""
    for element in database_array:
        clean_response += "{}, ".format(element[0])
    return clean_response[:-2]

@app.post("/medbot-api/")
async def read_message(message: Message):
    anon_text, entities = anonymize.anonymize_prompt(message.text)
    intent = to_sql.predict_intent(anon_text)
    entities = to_sql.extract_entities(anon_text)
    sql_query = to_sql.generate_sql(intent, entities)
    database_response = generate_result(intent, entities, sql_query)
    path = explainer.explain(message.text)

    return JSONResponse(
        content={"status": "success", "response_text": database_response, "explain_path": path},
        status_code=200
    )
