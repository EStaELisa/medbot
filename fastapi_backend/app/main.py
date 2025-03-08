import os
import psycopg2
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

from fastapi_backend.app.AnonymizationPipeline import anonymize
from fastapi_backend.app.questiontosql import to_sql
from fastapi_backend.app.XAI import explainer

# Database configuration
db_host = os.getenv("PGHOST", "db")
db_name = os.getenv("PGDATABASE", "postgres")
db_user = os.getenv("PGUSER", "postgres")
db_password = os.getenv("PGPASSWORD", "postgres")
db_port = os.getenv("PGPORT", "5432")


def connect_and_query(generated_query):
    """
    Executes a given SQL query on the configurated PostgreSQL database and returns the results

    Args:
        generated_query (str): SQL query to be executed.

    Returns:
        list: A list of tuples containing the query results

    This function established a connection to the database, executes the query, fetches the results
    and then closes the connection.
    """
    db_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port,
    }
    results = ""

    try:
        # Establish the connection
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Execute the query
        query = generated_query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

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
    """
    Generates a response based on the intent and entities extracted from the input text.

    Args:
        intent (str): The intent of the user's query.
        entities (list): The extracted entities relevant to the query.
        generated_query (str): The query generated based on the intent and entities.

    Returns:
        str: A formatted response based on the database results.
    """
    db_answer = connect_and_query(generated_query)
    clean_response = stringify_database_response(db_answer)
    response = ""
    if intent == "get_symptoms":
        response = f"The symptoms for {', '.join(entities)} are: {clean_response}"
    elif intent == "get_diagnose":
        response = f"Possible diagnoses for the symptoms {', '.join(entities)} are: {clean_response}"
    return response

class Message(BaseModel):
    """
    A Pydantic model representing the structure of an incoming user message.

    Attributes:
        text (str): The text of the incoming user message.
    """
    text: str

# Initialize FastAPI application
app = FastAPI()

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

def stringify_database_response(database_array):
    """
    Converts a database query result into a formatted string.

    Args:
        database_array (list of tuples): The raw query results from the database.

    Returns:
        str: A comma-separated string og the query results.
    """
    clean_response = ""
    for element in database_array:
        clean_response += "{}, ".format(element[0])
    return clean_response[:-2]

@app.post("/medbot-api/")
async def read_message(message: Message):
    """
    Processes an incoming user message, performs anonymization, intent recognition, entity extraction, SQL query generation
    and explanation creation.

    Args:
        message (Message): The user message containing the input text.

    Retunrs:
        JSONResponse: A JSON object containing the response text and explanation path.
    """
    anon_text, anon_entities = anonymize.anonymize_prompt(message.text)
    intent = to_sql.predict_intent(anon_text)
    entities = to_sql.extract_entities(anon_text)
    sql_query = to_sql.generate_sql(intent, entities)
    database_response = generate_result(intent, entities, sql_query)
    explanationid = explainer.explain(message.text, anon_text, anon_entities, sql_query)

    return JSONResponse(
        content={"status": "success", "response_text": database_response, "explain_path": explanationid},
        status_code=200
    )
@app.get("/explanation/{explanationid}")
async def show_explanation(explanationid):
    """
    Retrieves and displays an HTML explanation file for a given explanation ID.

    Args:
        explanationid (str): The unique identifier of the explanation.

    Returns:
        HTMLResponse: The explanation file content or a "File not found" message.
    """
    # Path to the HTML file
    html_file_path = Path("fastapi_backend/app/static/explanations/" + explanationid + ".html")

    # Read the HTML file
    if html_file_path.exists():
        html_content = html_file_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    else:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the API is running.

    Returns:
        dict: A JSON object indicationg the service status
    """
    return {"status": "healthy"}