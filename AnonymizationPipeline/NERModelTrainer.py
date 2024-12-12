from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, pipeline
from datasets import load_dataset
from transformers import DataCollatorForTokenClassification

class NERModelTrainer:
    def __init__(self, model_name, label_list, data_files):
        """
        Initialisiert das Modell, den Tokenizer und die Label-Mappings.

        :param model_name: Name des vortrainierten Modells.
        :param label_list: Liste der Labels (z. B. ['O', 'B-PER', 'I-PER', 'B-EMAIL', 'B-PHONE']).
        :param data_files: Pfade zu den Trainings- und Testdaten.
        """
        self.data_collator = None
        self.dataset = None
        self.trainer = None
        self.model_name = model_name
        self.label_list = label_list
        self.data_files = data_files

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)

        # Label-Mapping für das Modell konfigurieren
        self.id2label = {i: label for i, label in enumerate(self.label_list)}
        self.label2id = {label: i for i, label in enumerate(self.label_list)}
        self.model.config.id2label = self.id2label
        self.model.config.label2id = self.label2id

    def load_data(self):
        """
        Lädt den Datensatz im angegebenen Format.
        """
        self.dataset = load_dataset("conll2003", data_files=self.data_files)

    def train(self, output_dir, num_train_epochs=3, batch_size=16, learning_rate=2e-5):
        """
        Führt das Training des Modells durch.

        :param output_dir: Pfad zum Speichern der Trainingsergebnisse.
        :param num_train_epochs: Anzahl der Trainings-Epochen.
        :param batch_size: Größe der Batch.
        :param learning_rate: Lernrate.
        """
        self.data_collator = DataCollatorForTokenClassification(self.tokenizer)

        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_train_epochs,
            weight_decay=0.01,
            save_strategy="epoch",
            logging_dir="./logs",
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset["train"],
            eval_dataset=self.dataset["test"],
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
        )

        self.trainer.train()

    def save_model(self, save_path):
        """
        Speichert das trainierte Modell und den Tokenizer.

        :param save_path: Pfad zum Speichern des Modells.
        """
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

    def load_trained_model(self, load_path):
        """
        Lädt ein bereits trainiertes Modell für die Inferenz.

        :param load_path: Pfad zum trainierten Modell.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(load_path)
        self.model = AutoModelForTokenClassification.from_pretrained(load_path)

    def infer(self, text):
        """
        Führt Named Entity Recognition auf einem gegebenen Text aus.

        :param text: Eingabetext.
        :return: Liste erkannter Entitäten.
        """
        ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            grouped_entities=True
        )
        return ner_pipeline(text)