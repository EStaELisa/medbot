# import spacy

# # Load a pretrained NER model (or use a domain-specific model)
# nlp = spacy.load("en_core_sci_sm")  # Replace with a medical model like BioNER if available

# # Add domain-specific terms (optional)
# SYMPTOMS = ["fever", "chills", "shortness of breath", "low blood pressure", "cough", "fatigue", "nausea", "vomiting", "diarrhea", "headache", "muscle pain", "sore throat", "runny nose", "loss of taste", "loss of smell", "chest pain", "abdominal pain", "confusion", "seizures", "rash", "swelling", "redness", "bruising", "bleeding", "dizziness", "weakness", "numbness", "tingling", "blurred vision", "double vision", "hearing loss", "tinnitus", "palpitations", "irregular heartbeat", "chest tightness", "wheezing", "coughing up blood", "blood in urine", "blood in stool", "blood in vomit", "blood in sputum", "blood in saliva", "blood in mucus", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion",
#             "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion", "blood in exudate", "blood in effusion", "blood in pus", "blood in phlegm", "blood in discharge", "blood in fluid", "blood in drainage", "blood in secretion",]
# DIAGNOSES = ["sepsis", "pneumonia", "influenza", "diabetes", "heart attack", "stroke", "cancer", "COVID-19", "hypertension", "asthma", "COPD", "anemia", "migraine", "arthritis", "gout", "lupus", "fibromyalgia", "HIV", "hepatitis", "cirrhosis", "pancreatitis", "appendicitis", "diverticulitis", "gastroenteritis", "colitis", "ulcer", "GERD", "gallstones", "kidney stones", "UTI", "STD", "pregnancy", "menopause", "endometriosis", "PCOS", "fibroids", "ovarian cyst", "prostate cancer", "testicular cancer", "erectile dysfunction", "infertility", "pregnancy", "miscarriage", "stillbirth", "premature birth", "low birth weight", "birth defects", "down syndrome",
#              "autism", "cerebral palsy", "ADHD", "depression", "anxiety", "bipolar disorder", "schizophrenia", "PTSD", "OCD", "eating disorder", "alcoholism", "drug addiction", "smoking", "obesity", "anorexia", "bulimia", "diarrhea", "constipation", "nausea", "vomiting", "abdominal pain", "bloating", "gas", "heartburn", "indigestion", "food poisoning", "food allergy", "celiac disease", "Crohn's disease", "ulcerative colitis", "liver disease", "gallbladder disease", "pancreatic disease", "kidney disease", "bladder disease", "prostate disease", "testicular disease", "ovarian disease", "uterine disease", "cervical disease", "vaginal disease", "vulvar disease"]


# def extract_entity_spacy(query, intent):
#     doc = nlp(query)
#     if intent == "get_symptoms":
#         # Match diagnosis
#         for ent in doc.ents:
#             if ent.text.lower() in DIAGNOSES:
#                 return {"diagnosis": ent.text}
#     elif intent == "get_diagnose":
#         # Match symptoms
#         symptoms_found = [symptom for symptom in SYMPTOMS if symptom in query.lower()]
#         return {"symptoms": symptoms_found}
#     return None


import medspacy

# Lade MedSpaCy-Pipeline
nlp = medspacy.load()

SYMPTOMS = ["fever", "chills", "shortness of breath", "cough"]
DIAGNOSES = ["pneumonia", "COVID-19", "diabetes"]


def extract_entities_medspacy(text):
    doc = nlp(text)
    symptoms_found = []
    diagnoses_found = []

    for ent in doc.ents:
        if ent.text.lower() in SYMPTOMS:
            symptoms_found.append(ent.text)
        elif ent.text.lower() in DIAGNOSES:
            diagnoses_found.append(ent.text)

    return {"symptoms": symptoms_found, "diagnoses": diagnoses_found}


text = "The patient has fever and chills, and they might have pneumonia."
print(extract_entities_medspacy(text))
