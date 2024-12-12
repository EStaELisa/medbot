

from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, pipeline
from datasets import load_dataset
from transformers import DataCollatorForTokenClassification
from AnonymizationPipeline.NERModelTrainer import NERModelTrainer

# Beispielanwendung
if __name__ == "__main__":
    label_list = ["O", "B-PER", "I-PER", "B-EMAIL", "B-PHONE"]
    data_files = {
        "train": "path_to_train.txt",
        "test": "path_to_test.txt"
    }

    trainer = NERModelTrainer(
        model_name="xlm-roberta-large-finetuned-conll03-english",
        label_list=label_list,
        data_files=data_files
    )

    trainer.load_data()
    trainer.train(output_dir="./results", num_train_epochs=3)
    trainer.save_model("./finetuned_model")

    # Nach dem Training
    trainer.load_trained_model("./finetuned_model")
    text = "John Doe lives in Berlin and works for OpenAI. His phone number is 123-456-7890."
    entities = trainer.infer(text)

    for entity in entities:
        print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.2f}")
