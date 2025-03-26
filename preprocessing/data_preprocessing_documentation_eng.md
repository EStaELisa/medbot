# Data Preprocessing and Symptom Extraction 

### Contribution by: Zeineb Souiai

As part of our project, I was responsible for designing and implementing the data preprocessing pipeline. My goal was to extract meaningful and structured symptom information from unstructured medical text.

Initially, we explored the MIMIC dataset, but we ultimately decided to exclude it because it didn’t provide direct symptom-to-disease mappings that could be used for downstream machine learning tasks. Instead, we focused on the NHS dataset, which offered more suitable content for our use case.

## Process


### 1. Data Loading
CSV files scraped from the NHS website were loaded using `pandas`. These contained disease names and unstructured symptom descriptions.

### 2. Custom Stopword Filtering
A custom set of domain-specific stopwords was applied to remove irrelevant words that could interfere with symptom extraction. This included medical and generic terms like "include", "known", "cause", etc.

### 3. Lemmatization
The `WordNetLemmatizer` from NLTK was used to standardize tokens to their root form (e.g., "swollen" → "swelling").

### 4. Symptom Extraction

- **Phrase Matching**: Used a curated list of symptoms and phrases (e.g., "chest pain", "shortness of breath") for exact matching in preprocessed text.
- **Regex Matching**: Extracted patterns following constructs like "symptoms include", "symptoms such as", etc.
- **Compound Word Detection**: Implemented logic to catch meaningful multi-word terms with keywords like "pain" or "swelling", avoiding irrelevant matches.

### 5. Filtering Unusable Entries
- Rows with no meaningful symptoms or vague terms like "pain" or "flu" alone were removed.
- Diseases like "catarrh" were excluded due to lack of usable symptom data.

### 6. Data Cleanup and Output
- Symptoms were deduplicated and sorted by disease.
- Final dataset only included clean, structured disease–symptom entries, saved to CSV.

## Script Iterations
Throughout the project, I experimented with multiple Python scripts to refine the extraction logic and optimize results. Early versions like nhs_prep.py, and preprocessing.py were used to test different libraries and symptom-matching strategies. These versions helped me identify the limitations of certain tools and iteratively improve the logic. The final working implementation was consolidated in prep_symptom_to_disease.py, which contains the fully functional, optimized code used in the final pipeline.

## Final Remarks
The preprocessing and extraction pipeline developed contributed to structuring raw medical text into clean symptom–disease pairs, tailored for use in our chatbot’s database and downstream machine learning tasks. The process involved a combination of rule-based, pattern-based, and lexical techniques, all optimized to suit the specific characteristics of the NHS dataset.

This step was crucial for improving data quality and ensuring that further model training and querying could be based on reliable and relevant symptom information.
