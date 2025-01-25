import  pandas as pd


# loading the NHS dataset
nhs_data = pd.read_csv(r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\raw data\disease_symptoms.csv")

# cleaning text columns (specifically the name column)
def clean_text(text):
    if isinstance(text, str):
        text = text.lower().strip()
        return text
    
nhs_data['disease_cleaned'] = nhs_data['disease'].apply(clean_text)
nhs_data['symptom_cleaned'] = nhs_data['symptom'].apply(clean_text)

# grouping symptoms by disease
grouped_nhs = nhs_data.groupby('disease_cleaned')['symptom_cleaned'].apply(lambda x: ', '.join(x)).reset_index()

# renaming columns for clarity
grouped_nhs.columns = ['disease', 'symptom']

# saving the grouped data as a table
output_path = r"C:\Users\zeine\OneDrive\Documents\Projektstudium II\nhs_symptoms_diseases_table.csv"
grouped_nhs.to_csv(output_path, index= False)

print(f"Transformed NHS data saved to: {output_path}")

