from transformers import BertForSequenceClassification, BertTokenizer
from app.AnonymizationPipeline import (anonymize)
from app.XAI import intent_explanation, anonymization_explanation

def explain(text):
    model_path = "DeliaMo/ner_intent"
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    #text = "The patient Julia Meyer is suffering from fewer and chills, what could her diagnose be? Call her back at +491110020"
    anon_text, entities = anonymize.anonymize_prompt(text)
    anonymization_explanation.print_anon_text(anon_text)
    anonymization_explanation.explain_anonymization(entities)

    wrapper = intent_explanation.ModelWrapper(model, tokenizer, {"get_symptoms": 0, "get_diagnose": 1})
    return intent_explanation.lime_explanation(wrapper, anon_text)
