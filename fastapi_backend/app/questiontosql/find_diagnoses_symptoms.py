from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
from datasets import Dataset
from sklearn.model_selection import train_test_split
import json

# Load dataset
data_path = "symptom_diagnosis_dataset.json"
with open(data_path, "r") as f:
    dataset = json.load(f)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Data preparation


def prepare_data(data):
    tokenized_data = []
    for entry in data:
        text = entry["query"]
        tokens = tokenizer.tokenize(text)
        labels = ["O"] * len(tokens)

        # Mark entities
        for entity, label in entry.get("entities", []):
            entity_tokens = tokenizer.tokenize(entity)
            for i in range(len(tokens) - len(entity_tokens) + 1):
                if tokens[i:i+len(entity_tokens)] == entity_tokens:
                    labels[i] = "B-ENTITY"
                    for j in range(1, len(entity_tokens)):
                        labels[i+j] = "I-ENTITY"

        tokenized_data.append({"tokens": tokens, "labels": labels})
    return tokenized_data


prepared_data = prepare_data(dataset)

# Convert labels to indices
label_to_id = {"O": 0, "B-ENTITY": 1, "I-ENTITY": 2}
id_to_label = {v: k for k, v in label_to_id.items()}

for item in prepared_data:
    item["labels"] = [label_to_id[label] for label in item["labels"]]

# Split data into train and eval sets
train_data, eval_data = train_test_split(prepared_data, test_size=0.2)

train_dataset = Dataset.from_list(train_data)
eval_dataset = Dataset.from_list(eval_data)


def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        is_split_into_words=True,
        padding="max_length",
        max_length=128
    )
    labels = []
    for i, label in enumerate(examples["labels"]):
        label_ids = []
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)
            else:
                label_ids.append(label[word_id])
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs


train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
eval_dataset = eval_dataset.map(tokenize_and_align_labels, batched=True)

# Load the pretrained model
model = AutoModelForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(label_to_id))

# Data collator
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir="./ner_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("./ner_model")
tokenizer.save_pretrained("./ner_model")
