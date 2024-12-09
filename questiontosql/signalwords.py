import spacy

# Load a pretrained NER model (or use a domain-specific model)
nlp = spacy.load("en_core_sci_sm")  # Replace with a medical model like BioNER if available

# Add domain-specific terms (optional)
SYMPTOMS = ["fever", "chills", "shortness of breath", "low blood pressure"]
DIAGNOSES = ["sepsis", "pneumonia", "influenza", "diabetes"]


def extract_entity_spacy(query, intent):
    doc = nlp(query)
    if intent == "get_symptoms":
        # Match diagnosis
        for ent in doc.ents:
            if ent.text.lower() in DIAGNOSES:
                return {"diagnosis": ent.text}
    elif intent == "get_diagnose":
        # Match symptoms
        symptoms_found = [symptom for symptom in SYMPTOMS if symptom in query.lower()]
        return {"symptoms": symptoms_found}
    return None
