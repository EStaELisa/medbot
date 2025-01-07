# MIMIC database

To build a medical chatbot, a good and extensive dataset is crucial. One of the most comprehensive and freely available datasets is the MIMIC (Medical Information Mart for Intensive Care) dataset. The data is de-identified and includes data from over 40,000 ICU patients and over 60,000 hospital admissions [1]. The most recent MIMIC dataset is the MIMIC-IV dataset containing da from 2008-2019 [2].
I t provides information about the patient demographics (age, gender, ethnicity...), vital signs (heart rate, blood pressure, respiratory rate, etc., recorded over time), laboratory results (like blood/ urin tests or microbiology reports), medications (drug prescriptions, dosages, administration times), procedures (surgical procedures, imaging studies...), ICU stay information (as the length of stay, diagnoses, severity scores (e.g., APACHE), and mortality outcomes) and billing codes. Additionally, clinical notes are given that include unstructured text data, including physician notes, discharge summaries, and radiology reports [1].

Generally, the dataset is freely accessible, however, to access some of the datasets, specific requirements need to be met, ensuring the safety of the patient de-identification.
There are sample datasets without requirements such as the MIMIC-IV Clinical Database Demo (<https://physionet.org/content/mimic-iv-demo/2.2/>). However, that sample dataset does not contain the clinical notes which include key information such as the symptoms of the patient.

To get access to the full MIMIC-IV dataset you must make an account on PhysioNet and become a credential user [2]. For that you have to fill out a form including information about you, your supervisor and the project. Also, If you use LLM, you must indicate that you comply with the policy at the following link: <https://physionet.org/news/post/gpt-responsible-use>. For all datasets, take their specific license into account.

[1] Johnson, Alistair EW, et al. "MIMIC-IV, a freely accessible electronic health record dataset." Scientific data 10.1 (2023)

[2] <https://mimic.mit.edu/docs/about/>, 27.12.24
