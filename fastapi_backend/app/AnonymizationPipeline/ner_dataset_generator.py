import os.path
from sklearn.model_selection import train_test_split
from faker import Faker
import random


class SentenceGenerator:
    """
    Generates sentences using a variety of templates with fake personal and organizational data.
    """
    def __init__(self):
        """
        Initializes the SentenceGenerator class with a Faker instance to create fake data.
        """
        self.faker = Faker()
        self.diseases = ["Covid 19", "Diabetes", "Hypertension", "Influenza", "Asthma", "Migraine", "Pneumonia"]

    def generate_varied_sentence(self):
        """
        Generates a sentence using random templates and fake data.
        Returns:
            tuple: A tuple containing the generated sentence, name, company, city, email, and phone.
        """
        name = self.faker.name()
        company = self.faker.company()
        city = self.faker.city()
        email = self.faker.email()
        phone = self.faker.phone_number()
        disease = random.choice(self.diseases)
        templates = [
            f"{name} is a patient at {company} in {city}. They have a known history of {disease} and a fever of 40°C. Contact them at {email} or {phone}",
            f"Dr. {name} works at {company} located in {city} You can reach the doctor at {email} or {phone}",
            f"{name} is scheduled for an appointment at {company} in {city} They have irregular high blood preassure of 150/92 For inquiries, call {phone} or email {email}",
            f"Your test results show a chortisol level of 240 mg/dL. contact {name} at {company} in {city} via {email} or {phone}",
            f"If you have {disease} reach out to {name} at {company} in {city} for medical advice Email: {email} Phone: {phone}",
            f"{name} from {company} in {city} is available for consultation of your {disease} at {email} or {phone}",
            f"Patient {name} has a white blood cell count of 15000/uL can be contacted through {company} in {city} at {email} or {phone}",
            f"For further assistance with your {disease}, email {name} at {email} in {city} or call {phone}",
            f"{name} medical records are at {company} in {city} Contact: {email} {phone} They report to have {disease} and an A1C level of 8.5%.",
            f"{name} has an appointment at {company} in {city} Confirm via {email} or call {phone} They have a BMI of 32 and a history of {disease}",
            f"Please reach {name} at {company} in {city} for {disease} concerns Email: {email} Phone: {phone}",
            f"{name} from {company} in {city} can be contacted at {email} or {phone} for follow-up",
            f"Your next visit with {name} at {company} in {city} is scheduled. Contact: {email} {phone}",
            f"Dr. {name} from {company} in {city} is available at {email} or {phone} for consultation and specializes in {disease}",
            f"{name} records at {company} in {city} can be accessed through {email} or {phone} Their malaria test showed a parasite density of 0.8%",
            f"To reschedule, contact {name} at {company} in {city} via {email} or {phone}",
            f"The patient {name} at {company} in {city} got a Mini-Mental-State exam score of 22. Contace them via {email} Phone: {phone} ",
            f"{name} experienced a skin pH of 5.5, contact them at {company} in {city} via {email} or {phone}",
        ]
        sentence = random.choice(templates)
        return sentence, name, company, city, email, phone


class SentenceAnnotator:
    """
    Annotates sentences with Named Entity Recognition (NER) labels based on entities such as name, company, city, email, and phone.
    """
    @staticmethod
    def annotate_sentence(sentence, name, company, city, email, phone):
        """
        Annotates the words in a sentence with their corresponding NER labels.
        Args:
            sentence (str): The sentence to be annotated.
            name (str): The name of the person.
            company (str): The name of the company.
            city (str): The name of the city.
            email (str): The email address.
            phone (str): The phone number.
        Returns:
            list: A list of tuples containing words and their corresponding NER labels.
        """

        words = sentence.split()
        annotations = []

        word_entities = {
            'PER': name,
            'ORG': company,
            'GPE': city,
            'EMAIL': email,
            'PHONE': phone
        }

        for word in words:
            label = "0"  # Default label
            for entity_type, entity in word_entities.items():
                if word in entity.split():
                    label = entity_type
                elif word[:-1] in entity.split():
                    label = entity_type
                    break
            annotations.append((word, label))

        return annotations


class FileWriter:
    """
    Handles writing annotated data to files.
    """
    @staticmethod
    def write_to_file(annotated_data, file_name):
        """
        Writes annotated data to a file in the specified format.
        Args:
            annotated_data (list): Annotated data to be written.
            file_name (str): The name of the output file.
        """

        with open(file_name, 'w') as f:
            for sentence in annotated_data:
                for word, label in sentence:
                    f.write(f"{word} {label}\n")
                f.write("\n")


class DataProcessor:
    """
    Processes raw CoNLL-format data to merge entities spanning multiple tokens.
    """
    @staticmethod
    def process_file(input_filename, output_name):
        """
        Processes the raw CoNLL-format data file and merges multi-token entities.
        Args:
            input_filename (str): The name of the raw input file.
            output_name (str): The name of the processed output file.
        """
        with open(input_filename, 'r') as infile, open(output_name, 'w') as outfile:
            prev_lable = "0"
            entity_parts = []

            for line in infile:
                if line.strip() == "":
                    if entity_parts:
                        outfile.write(f"{' '.join(entity_parts)} {prev_lable}\n")
                        entity_parts = []
                    outfile.write("\n")
                    continue

                word, label = line.strip().split()
                if label == prev_lable and label != "0":
                    entity_parts.append(word)
                else:
                    if entity_parts:
                        outfile.write(f"{' '.join(entity_parts)} {prev_lable}\n")
                        entity_parts = []
                    if label != "0":
                        entity_parts.append(word)
                    else:
                        outfile.write(f"{word} {label}\n")
                prev_lable = label
            if entity_parts:
                outfile.write(f"{' '.join(entity_parts)} {prev_lable}\n")


if __name__ == "__main__":
    """
    Main script for generating, annotating, and processing NER training data.
    """

    generator = SentenceGenerator()
    annotator = SentenceAnnotator()
    writer = FileWriter()
    processor = DataProcessor()

    data = [generator.generate_varied_sentence() for _ in range(1000)]
    all_annotated_data = []
    for sentence, name, company, city, email, phone in data:
        annotated_sentence = annotator.annotate_sentence(sentence, name, company, city, email, phone)
        all_annotated_data.append(annotated_sentence)

    train_data, test_data = train_test_split(
        all_annotated_data, test_size=0.2, random_state=42
    )
    if not os.path.exists("data/ner_train_data.txt") or not os.path.exists("data/ner_test_data.txt"):
        FileWriter.write_to_file(train_data, "data/ner_train_data.txt")
        FileWriter.write_to_file(test_data, "data/ner_test_data.txt")
    else:
        print("Files already exist")
