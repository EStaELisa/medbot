from questiontosql.to_sql import handle_query, predict_intent, extract_entities
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


# Tests für handle_query


@pytest.mark.parametrize(
    "query, expected_sql",
    [
        (
            "What are the symptoms of pneumonia?",
            """
            SELECT Symptoms.name 
            FROM Symptoms
            JOIN Diagnoses ON Diagnoses.symptom_id = Symptoms.id
            WHERE Diagnoses.name IN ('pneumonia');
            """.strip()
        ),
        (
            "I have fever and chills, what could it be?",
            """
            SELECT Diagnoses.name 
            FROM Diagnoses
            JOIN Symptoms ON Symptoms.id = Diagnoses.symptom_id
            WHERE Symptoms.name IN ('fever', 'chills');
            """.strip()
        ),
        (
            "Tell me the symptoms of influenza.",
            """
            SELECT Symptoms.name 
            FROM Symptoms
            JOIN Diagnoses ON Diagnoses.symptom_id = Symptoms.id
            WHERE Diagnoses.name IN ('influenza');
            """.strip()
        ),
    ],
)
def test_handle_query(query, expected_sql):
    sql_query = handle_query(query)
    assert sql_query.strip() == expected_sql

# Tests für predict_intent


@pytest.mark.parametrize(
    "query, expected_intent",
    [
        ("What are the symptoms of pneumonia?", "get_symptoms"),
        ("I have fever and chills, what could it be?", "get_diagnose"),
        ("What might cause shortness of breath and nausea?", "get_diagnose"),
        ("Tell me the symptoms of influenza.", "get_symptoms"),
    ],
)
def test_predict_intent(query, expected_intent):
    intent = predict_intent(query)
    assert intent == expected_intent

# Tests für extract_entities


@pytest.mark.parametrize(
    "query, expected_entities",
    [
        ("What are the symptoms of pneumonia?", ["pneumonia"]),
        ("I have fever and chills, what could it be?", ["fever", "chills"]),
        ("What might cause shortness of breath and nausea?", ["shortness of breath", "nausea"]),
        ("Tell me the symptoms of influenza.", ["influenza"]),
    ],
)
def test_extract_entities(query, expected_entities):
    entities = extract_entities(query)
    assert set(entities) == set(expected_entities)  # Compare as sets for order-agnostic comparison
