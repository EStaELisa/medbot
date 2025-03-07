import pandas as pd
import os

def export_diseases_to_csv(input_file, output_dir):
    """
    Export each disease and its symptoms to separate CSV files.
    """
    df = pd.read_csv(input_file)
    
    os.makedirs(output_dir, exist_ok=True)
    
    df = df.groupby('disease')['symptom'].apply(' '.join).reset_index()
    
    for _, row in df.iterrows():
        disease = row['disease']
        filename = "".join(x for x in disease if x.isalnum() or x in (' ','-','_')).strip()
        output_file = os.path.join(output_dir, f"{filename}.csv")
        
        disease_df = pd.DataFrame({'disease': [disease], 'symptom': [row['symptom']]})
        disease_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "../data/nhs/merged_nhs_data_cleaned.csv"
    output_dir = "./diseases"
    
    export_diseases_to_csv(input_file, output_dir)
    print(f"Individual disease CSV files saved to {output_dir}")
