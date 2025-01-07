# BERT model

Since the search of a suitable dataset and project was time intensive, and the approval for the MIMIC dataset took some time, it was agreed to start with a simpler dataset/ approach.

A dataset mapping symptoms and diagnoses was scaped. The model should answer two questions: 1. Get the symptoms for a given diagnose and 2. Get the diagnose for given symptoms. Therefore, the model should first recognize the intent of the question, secondly extract the symptoms/ diagnoses in the question and put it in a SQL-query.

To get the intent of the question and to get the symptoms/ diagnoses a natural language processing (NLP) pipeline was built to train a BERT-based model.

To predict the intent of the question, a big dataset was generated with questions and the fitting label. The question either has a diagnose and wants the corresponding symptoms (label: get_diagnose) or contains symptoms to which a diagnose is searched (label: get_symptoms).
The data was split into a training and validation set. Text inputs are tokenized using the pre-trained BERT tokenizer. Tokenization splits the text into smaller components (tokens) and converts them to numerical representations suitable for the BERT model. The tokenized inputs are made compatible with PyTorch, parameters for the training are set and the model trained. The corresponding tests confirm a successful training.

The symptoms/ diagnoses in the question were detected as specific entities. A dataset was generated containing a question with a diagnose or symptoms and the desired entity. The text was converted into tokens and a label was assigned to each token: B-ENTITY (Begin-Entity): Marks the first token of an entity. I-ENTITY (Inside-Entity): Marks subsequent tokens of the same entity. O (Outside): Marks tokens not part of any entity. The dataset was split into training and validation data, the tokens aligned, the configurations set and the training started. The corresponding tests confirm a successful training.
Since the necessary power to train these models was not provided by my laptop, a Hetzner server was rented and configured with Pulumi so it could be boot up and down as needed (details in Hetzner-Pulumi-Template section).
