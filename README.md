# medbot

## Open project with dev container

download dockerdestop, start it

for vs code: blue button at the left button corner -> reload container

<https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container>


# Container builden
-Docker + Docker Compose installieren, dann Container buiolden mit:

docker-compose -f .devcontainer/docker-compose.yml up --build

SQL DB wird erstellt und per Skript (import_data_sql.py) gefüllt mit Daten aus nhs_disease_symptoms_processed_final.csv

Wenn Container läuft Zugriff auf SQL Konsole mit:
docker exec -it devcontainer-db-1 psql -U postgres

Dann Abfragen möglich, Bsp:

SELECT Symptoms 
FROM disease_symptoms
WHERE disease = 'flu';

SELECT disease
FROM disease_symptoms
WHERE Symptoms LIKE '%cough%';