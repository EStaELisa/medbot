from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Dein trainiertes Modell laden
checkpoint_path = "./results/checkpoint-954"
model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # Originalmodell oder Checkpoint

# Speicherpfad
save_directory = "./saved_model"

# Modell speichern
model.save_pretrained(save_directory)

# Tokenizer speichern
tokenizer.save_pretrained(save_directory)

print(f"Model and tokenizer saved in {save_directory}")
