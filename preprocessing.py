import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder

# Loading all datasets datasets
patients_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\patients.csv")
admissions_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\admissions.csv")
icd_diagnoses_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\icd_diagnoses.csv")
icd_procedures_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\icd_procedures.csv")
nhs_diseases_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_diseases.csv")
disease_symptoms_df = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\disease_symptoms.csv")

# MIMIC DATASET
# Step 1: Merging Patients + Admissions
merged_data = pd.merge(patients_df, admissions_df, on='SUBJECT_ID', how='inner')
print("Merged Patients + Admissions:", merged_data.head())

# Step 2: Merging with ICD Diagnoses
merged_data = pd.merge(merged_data, icd_diagnoses_df, on=['SUBJECT_ID', 'HADM_ID'], how='left')
print("After Adding Diagnoses:", merged_data.head())

# Optional: Cleaning text columns (e.g., DIAGNOSIS)
def clean_text(text):
    if isinstance(text, str):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
    return text

if 'DIAGNOSIS' in merged_data.columns:
    merged_data['DIAGNOSIS'] = merged_data['DIAGNOSIS'].apply(clean_text)

# Saving the final merged dataset
output_path = r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\partial_merged_data.csv"
merged_data.to_csv(output_path, index=False)
print(f"Partial merged dataset saved to: {output_path}")


# CLEANING AND PREPROCESSING

# Step 1: Cleaning and preprocessing the merged dataset from MIMIC

print("Merged Dataset Initial Shape:", merged_data. shape)

# 1.1 Handling missing values
print("Missing values in merged dataset:\n", merged_data.isnull().sum())

# filling missing values
merged_data['DIAGNOSIS'] = merged_data['DIAGNOSIS'].fillna('Unknown')
merged_data['ICD9_CODE'] = merged_data['ICD9_CODE'].fillna('No Code')


# 1.2 Standardizing Text Columns
def clean_text(text):
    if isinstance(text, str):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text) # removing special characters
    return text


# Applying to DIAGNOSIS column
merged_data['DIAGNOSIS'] = merged_data['DIAGNOSIS'].apply(clean_text)

# 1.3 Feature Engineering: Calculating Age at Admission
if 'ADMITTIME' in merged_data.columns and 'DOB' in merged_data.columns:
    merged_data['ADMITTIME'] = pd.to_datetime(merged_data['ADMITTIME'], errors='coerce')
    merged_data['DOB'] = pd.to_datetime(merged_data['DOB'], errors='coerce')
    merged_data['ADMIT_AGE'] = merged_data['ADMITTIME'].dt.year - merged_data['DOB'].dt.year

# removing any rows with negative or unrealistic ages
merged_data = merged_data[merged_data['ADMIT_AGE'] >= 0]

# 1.4 Saving Cleaned Merged Dataset
merged_output_path = r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\cleaned_merged_data.csv"
merged_data.to_csv(merged_output_path, index=False)
print(f'Cleaned merged dataset saved to: {merged_output_path}')

# NHS DATASET

# step1: cleaning text columns (specifically the name column)
def clean_text(text):
    if isinstance(text, str):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text

# cleaning the name column in NHS diseases and the disease column in disease symptoms
nhs_diseases_df['name_cleaned'] = nhs_diseases_df['name'].apply(clean_text)
disease_symptoms_df['disease_cleaned'] = disease_symptoms_df['disease'].apply(clean_text)

# step 2: merging datasets on cleaned disease name
merged_nhs_df = pd.merge(
    disease_symptoms_df,
    nhs_diseases_df,
    left_on='disease_cleaned',
    right_on='name_cleaned',
    how='left'
)

# step 3: handling missing values
merged_nhs_df['letter'] = merged_nhs_df['letter'].fillna('Unknown') # filling missing values at starting letters
merged_nhs_df['url_x'] = merged_nhs_df['url_x'].fillna(merged_nhs_df['url_y']) # using nhs url if missing in symptoms dataset
merged_nhs_df['url_x'] = merged_nhs_df['url_x'].fillna('Unknown URL')

# dropping redundant columns after merging
merged_nhs_df = merged_nhs_df.drop(columns=['name_cleaned', 'url_y'])


# step 4: saving the cleaned NHS diseases dataset
merged_nhs_output_path= r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\merged_nhs_data_cleaned.csv"
merged_nhs_df.to_csv(merged_nhs_output_path, index=False)
print(f'Cleaned NHS Diseases dataset saved to: {merged_nhs_output_path}')


