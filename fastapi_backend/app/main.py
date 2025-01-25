import os
import psycopg2
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.AnonymizationPipeline import anonymize
from app.questiontosql import to_sql

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

    if intent == "get_symptoms":
        response = f"The symptoms for {', '.join(entities)} are: {db_answer}"
    elif intent == "get_diagnose":
        response = f"Possible diagnoses for the symptoms {', '.join(entities)} are: {db_answer}"
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

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/message/")
async def read_message(message: Message):
    anon_text, entities = anonymize.anonymize_prompt(message.text)
    intent = to_sql.predict_intent(anon_text)
    entities = to_sql.extract_entities(anon_text)
    sql_query = to_sql.generate_sql(intent, entities)
    database_response = generate_result(intent, entities, sql_query)
    return JSONResponse(
        content={"status": "success", "intent": intent, "entities": entities, "sql_query": sql_query, "anon_text": database_response},
        status_code=200
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
