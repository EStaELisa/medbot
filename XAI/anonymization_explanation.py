
def explain_anonymization(entities):
    for entity in entities:
        print("Entity: ", entity['text'], "| Type:", entity['entity'], "| Confidence:", f"{entity['confidence']:.2f}")

def print_anon_text(text):
    print(text)