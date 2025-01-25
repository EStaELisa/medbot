import pytest
from fastapi_backend.app.questiontosql.transform_prediction_symp_dia import predict, transform_predictions

# Mock test cases for the predict function


@pytest.mark.parametrize(
    "text, expected",
    [
        ("The patient has fever and pneumonia.", [("fever", "B-ENTITY"), ("pneumonia", "B-ENTITY")]),
        ("Nausea and vomiting are common symptoms.", [("nausea", "B-ENTITY"), ("vomiting", "B-ENTITY")]),
        ("I suspect the patient has diabetes.", [("diabetes", "B-ENTITY")]),
    ],
)
def test_predict(text, expected):
    """
    Test the predict function to ensure it identifies entities correctly.
    """
    predictions = predict(text)
    # Normalize and compare predictions
    normalized_predictions = [(entity.lower(), label) for entity, label in predictions]
    expected_predictions = [(entity.lower(), label) for entity, label in expected]
    assert normalized_predictions == expected_predictions


# Mock test cases for the transform_predictions function
@pytest.mark.parametrize(
    "raw_predictions, expected",
    [
        (
            [("fever", "B-ENTITY"), ("pneumonia", "B-ENTITY")],
            {"entities": [{"text": "fever", "type": "B-ENTITY"}, {"text": "pneumonia", "type": "B-ENTITY"}]},
        ),
        (
            [("nausea", "B-ENTITY"), ("vomiting", "B-ENTITY")],
            {"entities": [{"text": "nausea", "type": "B-ENTITY"}, {"text": "vomiting", "type": "B-ENTITY"}]},
        ),
        (
            [("diabetes", "B-ENTITY")],
            {"entities": [{"text": "diabetes", "type": "B-ENTITY"}]},
        ),
    ],
)
def test_transform_predictions(raw_predictions, expected):
    """
    Test the transform_predictions function to ensure it transforms raw predictions correctly.
    """
    structured_data = transform_predictions(raw_predictions)
    assert structured_data == expected


# Integration test: Combining predict and transform_predictions
@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "The patient has fever and pneumonia.",
            {"entities": [{"text": "fever", "type": "B-ENTITY"}, {"text": "pneumonia", "type": "B-ENTITY"}]},
        ),
        (
            "Nausea and vomiting are common symptoms.",
            {"entities": [{"text": "nausea", "type": "B-ENTITY"}, {"text": "vomiting", "type": "B-ENTITY"}]},
        ),
    ],
)
def test_predict_and_transform(text, expected):
    """
    Test the integration of predict and transform_predictions functions.
    """
    raw_predictions = predict(text)
    structured_data = transform_predictions(raw_predictions)
    assert structured_data == expected
