
def explain_anonymization(entities):
    print("text, label, confidence")
    for entity in entities:
        print(entity['text'], ",", entity['entity'], ",", entity['confidence'])



