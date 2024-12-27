import unittest
from questiontosql.signalwords import extract_entity_spacy


class TestEntityExtraction(unittest.TestCase):

    def setUp(self):
        # Setup for test cases, e.g., initializing NLP model
        self.query_symptoms = "I have fever and chills, and I feel nauseous with a headache."
        self.query_diagnose = "I think I might have pneumonia or COVID-19."
        self.query_mixed = "I have been coughing and feel shortness of breath. Could it be asthma?"
        self.query_no_match = "I just need a regular health checkup."

    def test_get_symptoms(self):
        # Test extracting symptoms
        result = extract_entity_spacy(self.query_symptoms, "get_symptoms")
        self.assertIn("fever", result.get("symptoms"))
        self.assertIn("chills", result.get("symptoms"))
        self.assertIn("headache", result.get("symptoms"))
        self.assertIn("nausea", result.get("symptoms"))

    def test_get_diagnose(self):
        # Test extracting diagnoses
        result = extract_entity_spacy(self.query_diagnose, "get_diagnose")
        self.assertIn("pneumonia", result.get("diagnosis"))
        self.assertIn("COVID-19", result.get("diagnosis"))

    def test_mixed_query(self):
        # Test query with both symptoms and diagnoses
        result_symptoms = extract_entity_spacy(self.query_mixed, "get_symptoms")
        self.assertIn("cough", result_symptoms.get("symptoms"))
        self.assertIn("shortness of breath", result_symptoms.get("symptoms"))

        result_diagnose = extract_entity_spacy(self.query_mixed, "get_diagnose")
        self.assertIn("asthma", result_diagnose.get("diagnosis"))

    def test_no_match(self):
        # Test query with no symptoms or diagnoses
        result_symptoms = extract_entity_spacy(self.query_no_match, "get_symptoms")
        result_diagnose = extract_entity_spacy(self.query_no_match, "get_diagnose")
        self.assertEqual(result_symptoms, {"symptoms": []})
        self.assertIsNone(result_diagnose)


if __name__ == "__main__":
    unittest.main()
