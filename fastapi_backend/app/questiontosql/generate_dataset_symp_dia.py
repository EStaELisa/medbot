import random
import json

SYMPTOMS = [
    "fever", "chills", "cough", "fatigue", "shortness of breath", "headache",
    "nausea", "vomiting", "rash", "dizziness", "sore throat", "muscle pain",
    "loss of smell", "loss of taste", "abdominal pain", "diarrhea", "runny nose",
    "congestion", "chest pain", "tightness in chest", "palpitations", "weakness",
    "blurred vision", "tingling", "numbness", "swelling", "joint pain",
    "difficulty swallowing", "night sweats", "confusion", "seizures",
    "skin redness", "itching", "hair loss", "weight loss", "weight gain",
    "frequent urination", "increased thirst", "yellowing of skin", "dry mouth",
    "bloody stool", "coughing up blood", "blood in urine", "persistent pain",
    "dark urine", "light-colored stool", "hoarseness", "difficulty breathing",
    "snoring", "anxiety", "depression", "memory loss", "insomnia"
]
DIAGNOSES = [
    "pneumonia", "COVID-19", "diabetes", "hypertension", "stroke", "asthma",
    "anemia", "cancer", "migraine", "arthritis", "gastroenteritis", "COPD",
    "bronchitis", "tuberculosis", "heart failure", "arrhythmia", "coronary artery disease",
    "kidney stones", "urinary tract infection", "hepatitis", "liver cirrhosis",
    "pancreatitis", "appendicitis", "diverticulitis", "peptic ulcer",
    "gastritis", "irritable bowel syndrome", "Crohn's disease", "ulcerative colitis",
    "celiac disease", "gallstones", "thyroid dysfunction", "hyperthyroidism",
    "hypothyroidism", "multiple sclerosis", "parkinson's disease",
    "epilepsy", "alzheimer's disease", "lupus", "fibromyalgia", "gout",
    "psoriasis", "eczema", "lymphoma", "leukemia", "HIV/AIDS", "meningitis",
    "encephalitis", "sepsis", "otitis media", "sinusitis", "allergic rhinitis",
    "depression", "anxiety disorder", "bipolar disorder", "schizophrenia",
    "post-traumatic stress disorder", "eating disorder", "obesity",
    "anorexia nervosa", "bulimia nervosa", "sleep apnea", "osteoporosis",
    "rheumatoid arthritis", "peripheral neuropathy", "pancreatic cancer",
    "ovarian cancer", "breast cancer", "prostate cancer", "testicular cancer"
]

# get_symptoms
QUERY_TEMPLATES_DIAGNOSES = [
    "What are the symptoms of {}?",
    "Can you tell me the symptoms of {}?",
    "I want to know the symptoms of {}.",
    "What signs indicate {}?",
    "How can I identify {} based on symptoms?",
    "What should I look for if I suspect {}?",
    "What are the common signs of {}?",
    "Are there specific symptoms for {}?",
    "How do I know if someone has {}?",
    "What are the key indicators of {}?",
    "What are the major symptoms of {}?",
    "What are the initial symptoms of {}?",
    "Are there warning signs for {}?",
    "What are the tell-tale signs of {}?",
    "What should I watch out for with {}?",
    "How would I recognize {} symptoms?",
    "Can you provide the symptoms of {}?",
    "What happens to the body with {}?",
    "What are the usual symptoms for {}?",
    "Which symptoms are most common with {}?",
    "Could you describe the symptoms of {}?",
    "What happens when someone has {}?",
    "What are the physical signs of {}?",
    "Are there typical symptoms of {}?",
    "What does {} usually look like in terms of symptoms?",
    "How can one identify {} symptoms?",
    "What should I expect symptom-wise for {}?",
    "Which signs should I monitor for {}?",
    "What are the hallmark symptoms of {}?",
    "What are the diagnostic symptoms of {}?",
    "What are the symptoms that suggest {}?",
    "What are the symptoms that accompany {}?",
    "What are the symptoms that indicate {}?",
    "I have {}, what are the symptoms?",
    "My patient has {}, what can he expect?",
    "What are the symptoms of someone with {}?",
    "What might I experience with {}?",
    "What are the symptoms of a person with {}?",
]

# get diagnose
QUERY_TEMPLATES_SYMPTOMS = [
    "What might cause {}?",
    "I have {}, what could it be?",
    "What illnesses might include {}?",
    "Are {} symptoms of a specific condition?",
    "What disease could {} suggest?",
    "I’m experiencing {}, what’s the diagnosis?",
    "I am experiencing {}, what is the diagnosis?",
    "What medical conditions involve {}?",
    "What could {} point to?",
    "Could {} be related to any disease?",
    "What are the possible diagnoses for {}?",
    "I’m dealing with {}, any ideas?",
    "Could {} be a sign of something serious?",
    "What does {} typically mean?",
    "Does {} suggest a common illness?",
    "What might a doctor think if I have {}?",
    "What conditions match {}?",
    "Are there known conditions for {}?",
    "What diseases share {} as symptoms?",
    "What disorders are associated with {}?",
    "What could my {} mean medically?",
    "Are there common conditions for {}?",
    "What could be causing {}?",
    "Could {} indicate multiple issues?",
    "What health problems involve {}?",
    "I need help understanding {}, what could it be?",
    "Does {} align with any illnesses?",
    "What conditions are frequently associated with {}?",
    "What are the possible causes of {}?",
    "What are the potential diagnoses for {}?",
    "My symptoms include {}, what could it be?",
    "What are the possible health issues for {}?",
    "What are the possible diseases for {}?",
    "What are the possible illnesses for {}?",
    "What are the possible conditions for {}?",
    "My patient has {}, what could be the cause?",
    "My patient sufferes from {}, what could be the diagnose?",
    "What are the possible conditions for a patient with {}?",
    "What are the possible diseases for a patient with {}?",
]

# generate random dataset without intent
def generate_dataset(num_entries=1000):
    dataset = []
    for _ in range(num_entries // 2):  # half symptoms, half diagnoses
        # symptoms
        symptom = random.choice(SYMPTOMS)
        query = random.choice(QUERY_TEMPLATES_SYMPTOMS).format(symptom)
        dataset.append({
            "query": query,
            "entities": [(symptom, "ENTITY")]
        })

        # diagnoses
        diagnose = random.choice(DIAGNOSES)
        query = random.choice(QUERY_TEMPLATES_DIAGNOSES).format(diagnose)
        dataset.append({
            "query": query,
            "entities": [(diagnose, "ENTITY")]
        })
    return dataset

# generate dataset
dataset = generate_dataset(num_entries=2000)

# save dataset to file as JSON
with open("symptom_diagnosis_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("Dataset was generated and saved!")
