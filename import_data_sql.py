import os
import pandas as pd
import psycopg2
from io import StringIO

# Database connection details
db_host = os.getenv("PGHOST", "db")
db_name = os.getenv("PGDATABASE", "postgres")
db_user = os.getenv("PGUSER", "postgres")
db_password = os.getenv("PGPASSWORD", "postgres")
db_port = os.getenv("PGPORT", "5432")

# CSV file path
csv_file = "nhs_disease_symptoms_processed_final.csv"

def import_data_to_postgres():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cur = conn.cursor()

        # Create Symptoms table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Symptoms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE
            )
        """)

        # Create Diagnoses table with foreign key relationship to Symptoms (Unique constraint on Diagnoses.name)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Diagnoses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,  -- Ensuring diagnosis name is unique
                symptom_id INT REFERENCES Symptoms(id)
            )
        """)

        # Read the CSV with pandas
        df = pd.read_csv(csv_file)

        # Explicitly handle missing symptoms
        # Ensure no NaN values are being inserted into the database
        df['Symptoms'] = df['Symptoms'].apply(lambda x: None if pd.isna(x) else x)

        # Insert data into the Symptoms and Diagnoses tables
        for _, row in df.iterrows():
            disease = row['disease']
            symptoms = row['Symptoms']

            # Skip rows with missing symptom data
            if not symptoms:
                print(f"Skipping disease '{disease}' due to missing symptoms.")
                continue

            # Split symptoms by commas and insert them into the Symptoms table
            symptom_list = symptoms.split(',')

            # Insert each symptom and disease pairing
            for symptom in symptom_list:
                symptom = symptom.strip()  # Remove any extra spaces around symptoms
                if symptom:  # Only insert non-empty symptoms
                    # Insert symptom if not exists
                    cur.execute("INSERT INTO Symptoms (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (symptom,))

                    # Get the symptom ID for foreign key relationship
                    cur.execute("SELECT id FROM Symptoms WHERE name = %s", (symptom,))
                    symptom_id = cur.fetchone()[0]

                    # Insert disease with associated symptom (ensuring diagnosis is unique)
                    cur.execute("""
                        INSERT INTO Diagnoses (name, symptom_id) 
                        VALUES (%s, %s) 
                        ON CONFLICT (name) DO NOTHING
                    """, (disease, symptom_id))

        # Commit the changes
        conn.commit()
        print("Daten wurden erfolgreich importiert!")

    except Exception as e:
        print(f"Fehler beim Importieren der Daten: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    import_data_to_postgres()