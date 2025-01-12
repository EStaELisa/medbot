
import pandas as pd
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re




# loading the NHS dataset
nhs_data = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_symptoms_diseases_table.csv")


# initializing stopwords and lemmatizer
default_stopwords = set(stopwords.words('english'))

custom_stopwords = {
    'known', 'although', 'thought', 'usually', 'cause', 'causes',
    'example', 'include', 'result', 'symptoms', 'tend', 'may', 'might', 'will', 'see',
    'more', 'help', 'read', 'often', 'such', 'common', 'used', 'many', 'due'
}

stop_words = default_stopwords.union(custom_stopwords) - {'of', 'from', 'to'}
rake = Rake(stopwords=stop_words, max_length=3) # limiting phrase length
lemmatizer = WordNetLemmatizer()

# specific phrases for symptom extraction
specific_symptom_phrases = [
    'abdominal pain', 'back pain', 'chest pain', 'shortness of breath', 'high blood pressure',
    'dizziness', 'sweaty skin', 'clammy skin', 'loss of consciousness', 'fainting',
    'internal bleeding', 'pulsating sensation', 'persistent pain', 'haemorrhoids', 'anal fissures',
    "Acid and chemical burns",
    "Allergies",
    "Animal and human bites",
    "Ankle problems",
    "Back problems",
    "Blisters",
    "Bowel incontinence",
    "Breast pain",
    "Breast swelling in men",
    "Breathlessness and cancer",
    "Burns and scalds",
    "Calf problems",
    "Cancer-related fatigue",
    "Catarrh",
    "Chronic pain",
    "Constipation",
    "Cold sore",
    "Cough",
    "Cuts and grazes",
    "Chest pain",
    "Dehydration",
    "Diarrhoea",
    "Dizziness (lightheadedness)",
    "Dry mouth",
    "Earache",
    "Eating and digestion with cancer",
    "Elbow problems",
    "Farting",
    "Feeling of something in your throat (Globus)",
    "Fever in adults",
    "Fever in children",
    "Flu",
    "Foot problems",
    "Genital symptoms",
    "Hair loss and cancer",
    "Hay fever",
    "Headaches",
    "Hearing loss",
    "Hip problems",
    "Indigestion",
    "Insect bites and stings",
    "Itchy bottom",
    "Itchy skin",
    "Knee problems",
    "Living well with COPD",
    "Living with chronic pain",
    "Migraine",
    "Mouth ulcer",
    "Neck problems",
    "Nipple discharge",
    "Nipple inversion (inside out nipple)",
    "Nosebleed",
    "Pain and cancer",
    "Skin rashes in children",
    "Shortness of breath",
    "Shoulder problems",
    "Skin rashes in children",
    "Soft tissue injury advice",
    "Sore throat",
    "Stomach ache and abdominal pain",
    "Sunburn",
    "Swollen glands",
    "Testicular lumps and swellings",
    "Thigh problems",
    "Tick bites",
    "Tinnitus",
    "Toothache",
    "Urinary incontinence",
    "Urinary incontinence in women",
    "Urinary tract infection (UTI)",
    "Urinary tract infection (UTI) in children",
    "Vaginal discharge",
    "Vertigo",
    "Vomiting in adults",
    "Vomiting in children and babies",
    "Warts and verrucas",
    "Wrist, hand and finger problems",
    "Acid Reflux",
    "Airsickness",
    "Bad Breath",
    "Belching",
    "Bellyache",
    "Breathing Problems",
    "Bruises",
    "Choking",
    "Cluster Headache",
    "Cold (Temperature)",
    "Communication Disorders",
    "Contusions",
    "Dropsy",
    "Edema",
    "Flatulence",
    "Frostbite",
    "Frostnip",
    "Gas",
    "Gastrointestinal Bleeding",
    "Halitosis",
    "Heat Illness",
    "Hot (Temperature)",
    "Hypothermia",
    "Icterus",
    "Jaundice",
    "Kernicterus",
    "Language Problems",
    "Motion Sickness",
    "Pelvic Pain",
    "Pruritus",
    "Pyrexia",
    "Rare Diseases",
    "Raynaud Phenomenon",
    "Rectal Bleeding",
    "Sciatica",
    "Seasickness",
    "Speech and Communication Disorders",
    "Stammering",
    "Stuttering",
    "Sunstroke",
    "Syncope",
    "Tachypnea",
    "Tension Headache",
    "Thirst",
    "Tiredness",
    "Upset Stomach",
    "Urticaria",
    "Uterine Bleeding",
    "Vaginal Bleeding",
    "Vascular Headache",
    "Vasovagal Syncope",
    "Vestibular Diseases",
    "Weariness"
]

# Convert specific_symptom_phrases to lowercase
specific_symptom_phrases = [phrase.lower() for phrase in specific_symptom_phrases]


# preprocessing function
def preprocess_text(text):
    if pd.isnull(text):
        return ("")
    # lowercase
    text = text.lower()
    # removing punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text



# function to extract specific symptoms
def extract_specific_symptoms(text):
    processed_text = preprocess_text(text)
    extracted_symptoms = []

    # checking for specific phrases
    for phrase in specific_symptom_phrases:
        if phrase in processed_text:
            extracted_symptoms.append(phrase)

    # tokenizing, lemmatizing and extracting remaining symptoms
    tokens = word_tokenize(processed_text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # adding tokens matching any generic symptom words
    generic_symptoms = ['pain', 'swelling', 'rash', 'bleeding', 'fever', 'cough', 'fatigue', 'nausea',
        'vomiting', 'dizziness', 'weakness', 'inflammation' ]

    for token in tokens:
        if token in generic_symptoms and token not in extracted_symptoms:
            extracted_symptoms.append(token)
    return ", ".join(extracted_symptoms)



# applying symptom extraction
nhs_data['Symptoms'] = nhs_data['symptom'].apply(extract_specific_symptoms)

# retaining only necessary columns
final_data = nhs_data[['disease','Symptoms']]

# saving the results to a new file
output_file_path = r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_symptoms_diseases_symptoms_processed_final.csv"
final_data.to_csv(output_file_path, index=False)

print(f"Keyword extraction completed. Results saved to :{output_file_path}")
