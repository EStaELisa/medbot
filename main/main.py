from AnonymizationPipeline import anonymize
from XAI import anonymization_explanation

def main():
    text = input()
    anon_text, entities = anonymize.anonymize_prompt(text)
    print(anon_text)
    anonymization_explanation.explain_anonymization(entities)


if __name__ == "__main__":
    main()