import os
import webbrowser

from AnonymizationPipeline import anonymize
from XAI import anonymization_explanation, intent_explanation
from tests.test_questiontosql import test_intent
from transformers import BertForSequenceClassification, BertTokenizer


def main():
    MODEL_PATH = "DeliaMo/ner_intent"
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)

    text = "The patient Julia Meyer is suffering from fewer and chills, what could her diagnose be? Call her back at +491110020"
    anon_text, entities = anonymize.anonymize_prompt(text)
    print(anon_text)
    anonymization_explanation.explain_anonymization(entities)

    wrapper = intent_explanation.ModelWrapper(model, tokenizer, {"get_symptoms": 0, "get_diagnose": 1})
    intent_explanation.lime_explanation(wrapper, anon_text)

if __name__ == "__main__":
    main()