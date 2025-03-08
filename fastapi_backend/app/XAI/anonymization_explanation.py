def explain_anonymization(entities):
    """
    Iterates through the given entities, reads the confidence scores and gives an explanation what the scores mean.
    """
    for entity in entities:
        confidence = entity['confidence']
        if confidence > 0.9:
            explanation = "The model is very confident."
        elif confidence > 0.7:
            explanation = "The model is somewhat confident, but there is some uncertainty."
        else:
            explanation = "The model is not very confident; this could be a random prediction."

        print(f"Entity: {entity['text']} | Type: {entity['entity']} | Confidence: {confidence:.2f} | {explanation}")


def print_anon_text(text):
    """
    Print anonymized text.
    """
    print(text)