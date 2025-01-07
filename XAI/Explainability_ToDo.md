# Anonymization Model
- [X] Anzeigen, welche Entities gefunden wurden
- [X] Confidence Scores für jede Entity anzeigen
- [ ] (Ausgabe überarbeiten)
Beispiel:
```
Detected Entities and Confidence Scores:
Entity: 'John Smith' | Type: <PERSON> | Confidence: 0.94
Entity: 'Boston' | Type: <LOCATION> | Confidence: 0.89
```
- [X] Anonymisierten String anzeigen
# Intent Model
- [ ] Wörter anzeigen, die für den Intent wichtig sind
- [ ] Attention Maps / Saliency Maps, um anzuzeigen,  auf welchen Teil des Inputs sich das Model fokussiert
- [ ] (Natural Language Summary)
## SQL-Query 
- [ ] SQL-Query anzeigen und / oder dazu passenden Text
Beispiel:
```SQL
SELECT symptoms FROM diseases WHERE disease = 'flu'; 
```
```
The system is looking up symptoms associated with 'flu' in the database.
```
## Datenbank Ergebnis 
- [ ] Zuverlässigkeit des Ergebnisses anzeigen
# Natural Language Explanation
- [ ] Mapping Explanation: Anzeigen, wie das System Ergebnisse aus der DB in natural language umwandelt
- [ ] Möglichkeit, die Daten anzuschauen und den angezeigten Text 
Beispiel:
```
Database result: {symptom1: 'fever', symptom2: 'cough'}
Output: "The most common symptoms are fever and cough."
Explain: “The system prioritized symptoms with high prevalence and aligned them in a user-friendly order.”
```
# Optional
- Falls wir eine UI haben, können wir ein Explanation Dashboard einbauen, in dem alle Explanations aufgelistet werden. Das könnte hinter einem "Explain" Button liegen.
- Alternativ: Logging, sodass die Explanations jeweils auf der Konsole ausgegeben werden