
import pandas as pd
from rake_nltk import Rake
from nltk.corpus import stopwords
import nltk

# downloading NLTK stopwords
nltk.download('stopwords')

# loading the NHS dataset
nhs_data = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_symptoms_diseases_table.csv")


# initializing RAKE for keyword extraction
default_stopwords = set(stopwords.words('english'))

# extending stopwords for domain specific cleanup
custom_stopwords = {
    'known', 'although', 'thought', 'usually', 'cause', 'causes',
    'example', 'include', 'result', 'symptoms', 'tend', 'may', 'might', 'will', 'see',
    'more', 'help', 'read', 'often', 'such', 'common', 'used', 'many', 'due'
}

stop_words = default_stopwords.union(custom_stopwords) - {'of', 'from', 'to'}
rake = Rake(stopwords=stop_words, max_length=3) # limiting phrase length

# function for cleaning and summarizing symptoms
def clean_and_summarize(text):
    if pd.isnull(text):
        return ""
    sentences = text.split(".")
    summary = ".".join(sentences[:3]) # limiting to the first 3 sentences
    return summary.strip()

# function for extracting keywords using RAKE
def extract_keywords(symptoms_text):
    if pd.isnull(symptoms_text): # handling missing symptoms
        return ""
    rake.extract_keywords_from_text(symptoms_text)
    return ', '.join(rake.get_ranked_phrases()[:10]) # extracting top 10 keywords

# function to classify extracted keywords into causes or symptoms
def classify_keywords(keywords):
    if pd.isnull(keywords):
        return "", ""
    
    causes_keywords = {
        'cause', 'causes', 'risk', 'factor', 'leads,' 'because', 'due', 'results', 'linked', 'smoking',  'diet', 'genetic', 'lifestyle', 'environment', 'exposure', 'infection',
        'inherited', 'associated with', 'deficiency', 'contributes', 'related to'
        }
    symptoms_keywords = {
'symptom', 'symptoms', 'indicates', 'suggests', 'shows', 'associated', 'related',
        'pain', 'swelling', 'rash', 'bleeding', 'fever', 'cough', 'fatigue', 'nausea', 
        'vomiting', 'dizziness', 'weakness', 'inflammation'        }

    causes = []
    symptoms = []

    for keyword in keywords.split(','):
        keyword = keyword.strip().lower()
        if any (cause in keyword for cause in causes_keywords):
            causes.append(keyword)
        elif any(symptom in keyword for symptom in symptoms_keywords):
            symptoms.append(keyword)
        else:
            # defaulting to symptoms if there is no match
            symptoms.append(keyword)

    return ", ".join(causes), ", ".join(symptoms)



# cleaning and summarizing the symptom column
nhs_data['symptom_cleaned'] = nhs_data['symptom'].apply(clean_and_summarize)

# applying the keyword extraction
nhs_data['Extracted Keywords'] = nhs_data['symptom'].apply(extract_keywords)

# dropping the initial symptom column for clarity
nhs_data = nhs_data[['disease', 'symptom_cleaned', 'Extracted Keywords']]

# categorizing extracted keywords into causes and symptoms
nhs_data[['Causes', 'Symptoms']] = nhs_data['Extracted Keywords'].apply(
    lambda x: pd.Series(classify_keywords(x))
)

# final data columns
nhs_data = nhs_data[['disease', 'symptom_cleaned', 'Causes', 'Symptoms']]

# saving the results to a new file
output_file_path = r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_symptoms_diseases_with_keywords.csv"
nhs_data.to_csv(output_file_path, index=False)

print(f"Keyword extraction completed. Results saved to :{output_file_path}")
