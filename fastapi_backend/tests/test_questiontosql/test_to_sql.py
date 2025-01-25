import pytest

from fastapi_backend.app.questiontosql.to_sql import predict_intent, extract_entities, generate_sql


# **Test predict_intent**


@pytest.mark.parametrize(
    "query, expected_intent",
    [
        ("What are the symptoms of pneumonia?", "get_symptoms"),
        ("I have fever and chills, what could it be?", "get_diagnose"),
        ("Tell me the symptoms of flu.", "get_symptoms"),
        ("What could nausea and headache mean?", "get_diagnose"),
    ],
)
def test_predict_intent(query, expected_intent):
    intent = predict_intent(query)
    assert intent == expected_intent


# **Test extract_entities**
@pytest.mark.parametrize(
    "query, expected_entities",
    [
        ("What are the symptoms of pneumonia?", ["pneumonia"]),
        ("I have fever and chills, what could it be?", ["fever", "chills"]),
        ("What could cause nausea and headache?", ["nausea", "headache"]),
        ("Tell me the symptoms of influenza.", ["influenza"]),
    ],
)
def test_extract_entities(query, expected_entities):
    entities = extract_entities(query)
    assert set(entities) == set(expected_entities)  # Order-independent comparison


# **Test generate_sql**
@pytest.mark.parametrize(
    "intent, entities, expected_sql",
    [
        (
            "get_symptoms",
            ["pneumonia"],
            """
            SELECT Symptoms.name 
            FROM Symptoms
            JOIN Diagnoses ON Diagnoses.symptom_id = Symptoms.id
            WHERE Diagnoses.name IN ('pneumonia');
            """.strip(),
        ),
        (
            "get_diagnose",
            ["fever", "chills"],
            """
            SELECT Diagnoses.name 
            FROM Diagnoses
            JOIN Symptoms ON Symptoms.id = Diagnoses.symptom_id
            WHERE Symptoms.name IN ('fever', 'chills');
            """.strip(),
        ),
    ],
)
def test_generate_sql(intent, entities, expected_sql):
    sql_query = generate_sql(intent, entities)
    # Normalize SQL strings for comparison
    normalized_sql = " ".join(sql_query.strip().split())
    normalized_expected_sql = " ".join(expected_sql.strip().split())
    assert normalized_sql == normalized_expected_sql


# **Test handle_query**
# @pytest.mark.parametrize(
#     "query, expected_response",
#     [
#         (
#             "What are the symptoms of pneumonia?",
#             """
#             SELECT Symptoms.name
#             FROM Symptoms
#             JOIN Diagnoses ON Diagnoses.symptom_id = Symptoms.id
#             WHERE Diagnoses.name IN ('pneumonia');
#             """.strip(),
#         ),
#         (
#             "I have fever and chills, what could it be?",
#             """
#             SELECT Diagnoses.name
#             FROM Diagnoses
#             JOIN Symptoms ON Symptoms.id = Diagnoses.symptom_id
#             WHERE Symptoms.name IN ('fever', 'chills');
#             """.strip(),
#         ),
#         (
#             "What are the symptoms?",
#             "No entity found.",
#         ),
#     ],
# )
# def test_handle_query(query, expected_response):
#     response = handle_query(query)
#     # Normalize SQL strings or compare error messages
#     if "SELECT" in expected_response:
#         normalized_response = " ".join(response.strip().split())
#         normalized_expected_response = " ".join(expected_response.strip().split())
#         assert normalized_response == normalized_expected_response
#     else:
#         assert response == expected_response
