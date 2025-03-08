from lime.lime_text import LimeTextExplainer
import torch



class ModelWrapper:
    """
    A wrapper class for a BERT-based sequence classification model to explain classification and probability
    predictions.

    Attributes:
        model (BertSequenceClassification): The pre-trained BERT model for classification.
        tokenizer (BertTokenizer): The tokenizer used for text preprocessing.
        label_map (dict): A mapping of intent labels to numeric labels.
        reverse_label_map (dict): A reversed mapping from numerical indiced to intent labels.
    """
    def __init__(self, model, tokenizer, label_map):
        """
        Initializes the ModelWrapper with a BERT model, tokenizer and label mappings.

        Args:
            model (BertSequenceClassification): The pre-trained BERT model for classification.
            tokenizer (BertTokenizer): The tokenizer used for text preprocessing.
            label_map (dict): A mapping of intent labels to numeric labels.
        """

        self.model = model
        self.tokenizer = tokenizer
        self.label_map = label_map
        self.reverse_label_map = {v: k for k, v in label_map.items()}

    def predict_proba(self, texts):
        """
        Predicts probabilities for each intent label for a given list of texts.

        Args:
            texts (list of str): A list of input texts.

        Returns:
            numpy.ndarray: A 2D array where each row corresponds to the probability distribution over the intent
            labels for a given input text.
        """
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits.detach().numpy()
        probs = torch.nn.functional.softmax(torch.tensor(logits), dim=-1).numpy()
        return probs

def lime_explanation(model_wrapper, text):
    """
    Generates an explanation for a given text input using LIME.

    Args:
        model_wrapper (ModelWrapper): An instance of the ModelWrapper to perform intent classification
        text (str): The input text to be explained.

    Returns:
        str: An HTML representation of the LIME explanation.

    This function uses LIME to analyze the model's decision process by perturbing the input text and observing
    how the predictions change, highlighting the most important  words influencing the classification.
    """
    explainer = LimeTextExplainer(class_names=list(model_wrapper.label_map.keys()))

    explanation = explainer.explain_instance(
        text,
        model_wrapper.predict_proba,
        num_features=5,
        num_samples=100
    )
    return explanation.as_html()
