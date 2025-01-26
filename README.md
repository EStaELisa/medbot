# medbot

## Projektbeschreibung
medbot ist eine Webanwendung, bestehend aus Frontend, Backend, Datenbank und einem Dataimporter, die Symptome oder 
Krankheiten erkennen kann. Dafür nutzt sie Natural Language Processing (BERT) und erkennt den Intent der Frage. 
Anschließend wird eine passende SQL Anfrage gebaut und in der Datenbank gesucht. Die Eingabe wird anonymisiert, sodass
die Privatsphäre der Nutzer\*innen gewahrt ist. Hinterher erhalten Nutzer\*innen noch eine Explanation, um die Entscheidungen
des Bots nachvollziehen zu können.

## Voraussetzungen
- docker und docker compose müssen installiert sein
- docker muss laufen

## Projekt laufen lassen
Im Hauptordner (medbot) folgenden Befehl ausführen:
`docker compose -f .dockerisation/docker-compose.yml up --build`
Wenn die Zeile erscheint: `frontend-1  |  ✓ Ready in xxxxxx`, kann die Anwendung genutzt werden.

## Software verwenden
- Frontend ist erreichbar über: http://localhost:3000
- Im Chatfenster kann eine Anfrage in Englisch gestellt werden. Mit Enter oder dem Symbol unten rechts absenden.
- Der Bot braucht eine Weile, bis er die Antwort berechnet hat und sie erscheint.
- Im Antwort-Chatfeld des Bots gibt es ein ? Symbol, über das die jeweilige Explanation aufgerufen werden kann.

## Troubleshooting
- Sollte der Port 1337 belegt sein, den Docker für psql braucht, kann in der Datei .dockerisation/docker-compose.yaml die linke Zahl in Zeile 70 geändert werden.
