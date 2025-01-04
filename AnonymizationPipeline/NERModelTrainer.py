import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, pipeline
from datasets import Dataset
from transformers import DataCollatorForTokenClassification
import torch


class NERModelTrainer:
    def __init__(self, model_name, label_list, data_files):
        """
        Initializes the model, tokenizer, and label mappings.

        :param model_name: Name of the pre-trained model.
        :param label_list: List of labels (e.g., ['O', 'B-PER', 'I-PER', 'EMAIL', 'PHONE']).
        :param data_files: Paths to training and test data files.
        """
        self.model_name = model_name
        self.label_list = label_list
        self.data_files = data_files
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.label_list),  # Set the correct number of labels
            ignore_mismatched_sizes=True  # Ignore size mismatches
        )

        # Reinitialize the classifier layer to match your label set
        self.model.classifier = torch.nn.Linear(
            self.model.config.hidden_size, len(self.label_list)
        )

        # Setup label mappings
        self.id2label = {i: label for i, label in enumerate(label_list)}
        self.label2id = {label: i for i, label in enumerate(label_list)}

        self.model.config.id2label = self.id2label
        self.model.config.label2id = self.label2id

        # Initialize placeholders for dataset, trainer, etc.
        self.dataset = None
        self.data_collator = DataCollatorForTokenClassification(self.tokenizer)

    def load_data(self):
        """
        Loads the dataset from the provided file paths and tokenizes the data.
        """
        train_data = self.parse_ner_file(self.data_files["train"])
        test_data = self.parse_ner_file(self.data_files["test"])

        # Create train and test datasets
        train_dataset = Dataset.from_dict(train_data)
        test_dataset = Dataset.from_dict(test_data)

        # Tokenize and align labels for both train and test datasets
        self.dataset = {
            "train": train_dataset.map(self.tokenize_and_align_labels, batched=True),
            "test": test_dataset.map(self.tokenize_and_align_labels, batched=True)
        }

    def parse_ner_file(self, file_path):
        """
        Parses a CoNLL-style file and returns token-tag pairs.

        :param file_path: Path to the input CoNLL-style file.
        :return: Dictionary with "tokens" and "ner_tags".
        """
        tokens, ner_tags = [], []
        sentence_tokens, sentence_tags = [], []

        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    if sentence_tokens:
                        tokens.append(sentence_tokens)
                        ner_tags.append(sentence_tags)
                    sentence_tokens, sentence_tags = [], []
                else:
                    word, tag = line.split()
                    sentence_tokens.append(word)
                    sentence_tags.append(tag)

        return {"tokens": tokens, "ner_tags": ner_tags}

    def tokenize_and_align_labels(self, examples):
        """
        Tokenizes input texts and aligns labels with the tokenized input.

        :param examples: Dictionary containing 'tokens' and 'ner_tags'.
        :return: Tokenized input with aligned labels.
        """
        tokenized_inputs = self.tokenizer(
            examples["tokens"],
            truncation=True,
            padding=True,
            is_split_into_words=True
        )

        aligned_labels = []
        for i, labels in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            aligned_labels.append([
                -100 if word_id is None else self.label2id[labels[word_id]] if word_id < len(labels) else -100
                for word_id in word_ids
            ])

        tokenized_inputs["labels"] = aligned_labels
        return tokenized_inputs

    def train(self, output_dir, num_train_epochs=3, batch_size=16, learning_rate=2e-5):
        """
        Trains the model.

        :param output_dir: Path to save the model and training results.
        :param num_train_epochs: Number of training epochs.
        :param batch_size: Batch size for training.
        :param learning_rate: Learning rate for training.
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",  # Evaluate at the end of each epoch
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_train_epochs,
            weight_decay=0.01,
            save_strategy="epoch",
            logging_dir="./logs"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset["train"],
            eval_dataset=self.dataset["test"],
            tokenizer=self.tokenizer,
            data_collator=self.data_collator
        )

        trainer.train()

    def save_model(self, save_path):
        """
        Saves the trained model and tokenizer.

        :param save_path: Path to save the model.
        """
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

    def load_trained_model(self, load_path):
        """
        Loads a pre-trained model for inference.

        :param load_path: Path to the trained model.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(load_path)
        self.model = AutoModelForTokenClassification.from_pretrained(load_path)

    def infer(self, text):
        """
        Performs Named Entity Recognition on a given text.

        :param text: Input text for inference.
        :return: List of detected entities.
        """
        ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            grouped_entities=True
        )
        return ner_pipeline(text)

    def evaluate(self):
        """
        Evaluates the model on the test set.

        :return: Evaluation results.
        """
        trainer = Trainer(
            model=self.model,
            tokenizer=self.tokenizer,
            data_collator=self.data_collator
        )
        results = trainer.evaluate(self.dataset["test"])
        print("Evaluation results:", results)
        return results


if __name__ == "__main__":
    pretrained_model = "dbmdz/bert-large-cased-finetuned-conll03-english"
    label_list = ["0", "B-PER", "I-PER", "ORG", "GPE", "EMAIL", "PHONE"]
    data_files = {
        "train": "data/ner_train_data.txt",
        "test": "data/ner_test_data.txt"
    }

    # Create an instance of NERModelTrainer
    trainer = NERModelTrainer(pretrained_model, label_list, data_files)

    # Load and preprocess data
    trainer.load_data()

    # Train the model
    trainer.train(output_dir="ner_training", num_train_epochs=3, batch_size=16, learning_rate=5e-5)

    # Save the trained model
    os.makedirs("data/ner_finetuned_model", exist_ok=True)
    trainer.save_model("data/ner_finetuned_model")

    # Evaluate the model
    evaluation_results = trainer.evaluate()
