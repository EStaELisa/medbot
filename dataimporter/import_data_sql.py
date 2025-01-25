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
csv_file = "data/nhs_disease_symptoms_processed_final.csv"

def import_data_to_postgres():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()

    # Check if the table already exists
    cur.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = 'disease_symptoms'
        )
    """)
    table_exists = cur.fetchone()[0]

    if table_exists:
        print("Daten sind schon im System!")
    else:
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE disease_symptoms (
                id SERIAL PRIMARY KEY,
                disease VARCHAR(255) NOT NULL,
                symptoms TEXT NOT NULL
            )
        """)

        # Read the CSV with pandas
        df = pd.read_csv(csv_file)

        # Prepare the data for import
        output = StringIO()
        for _, row in df.iterrows():
            # Corrected column names
            line = f"{row['disease']}\t{row['Symptoms']}\n"
            output.write(line)

        output.seek(0)

        # Import data with tab as the delimiter
        cur.copy_from(output, 'disease_symptoms', columns=('disease', 'symptoms'), sep='\t')
        conn.commit()
        print("Daten wurden erfolgreich importiert!")

    cur.close()
    conn.close()

if __name__ == "__main__":
    import_data_to_postgres()