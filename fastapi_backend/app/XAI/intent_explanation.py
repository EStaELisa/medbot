import webbrowser

from lime.lime_text import LimeTextExplainer
import os
import torch
import uuid


class ModelWrapper:
    def __init__(self, model, tokenizer, label_map):
        self.model = model
        self.tokenizer = tokenizer
        self.label_map = label_map
        self.reverse_label_map = {v: k for k, v in label_map.items()}

    def predict_proba(self, texts):
        """
        Takes a list of texts and return probabilities for each label
        """
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits.detach().numpy()
        probs = torch.nn.functional.softmax(torch.tensor(logits), dim=-1).numpy()
        return probs

def lime_explanation(model_wrapper, text):
    explainer = LimeTextExplainer(class_names=list(model_wrapper.label_map.keys()))

    explanation = explainer.explain_instance(
        text,
        model_wrapper.predict_proba,
        num_features=5,
        num_samples=100
    )

    explanationid = uuid.uuid4()
    explanation_path = "app/static/explanations/" + str(explanationid) + ".html"
    explanation.save_to_file(explanation_path)
    return str(explanationid)