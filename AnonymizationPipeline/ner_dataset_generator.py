from faker import Faker
import random

faker = Faker()

def generate_varied_sentence():
    name = faker.name()
    company = faker.company()
    city = faker.city()
    email = faker.email()
    phone = faker.phone_number()
    templates = [
        f"{name} is a patient at {company} in {city} Contact them at {email} or {phone}",
        f"Dr. {name} works at {company} located in {city} You can reach the doctor at {email} or {phone}",
        f"{name} is scheduled for an appointment at {company} in {city} For inquiries, call {phone} or email {email}",
        f"To discuss your test results contact {name} at {company} in {city} via {email} or {phone}",
        f"Reach out to {name} at {company} in {city} for medical advice Email: {email} Phone: {phone}",
        f"{name} from {company} in {city} is available for consultation at {email} or {phone}",
        f"Patient {name} can be contacted through {company} in {city} at {email} or {phone}",
        f"For further assistance, email {name} at {email} in {city} or call {phone}",
        f"{name}'s medical records are at {company} in {city} Contact: {email} {phone}",
        f"{name} has an appointment at {company} in {city} Confirm via {email} or call {phone}",
        f"Please reach {name} at {company} in {city} for health concerns Email: {email} Phone: {phone}",
        f"{name} from {company} in {city} can be contacted at {email} or {phone} for follow-up",
        f"Your next visit with {name} at {company} in {city} is scheduled. Contact: {email} {phone}",
        f"Dr. {name} from {company} in {city} is available at {email} or {phone} for consultation",
        f"{name}'s records at {company} in {city} can be accessed through {email} or {phone}",
        f"To reschedule, contact {name} at {company} in {city} via {email} or {phone}",
        f"Reach out to {name} at {company} in {city} for test results Email: {email} Phone: {phone}",
        f"For any medical inquiries, contact {name} at {company} in {city} via {email} or {phone}",
    ]
    sentence = random.choice(templates)
    return sentence, name, company, city, email, phone


def prepare_sentence(sentence):
    words = sentence.split()
    return words


def annotate_sentence(sentence, name, company, city, email, phone):
    words = prepare_sentence(sentence)
    annotations = []
    names = name.split()


    word_entities = {
        'B-PER': names[0],
        'I-PER': names[1],
        'ORG': company,
        'GPE': city,
        'EMAIL': email,
        'PHONE': phone
    }

    for word in words:
        label = "0"
        for entity_type, entity in word_entities.items():
            if word in entity.split():
                label = entity_type
            elif word[:-1] in entity.split():
                label = entity_type
                break
        annotations.append((word, label))

    return annotations


def convert_to_conll(annotated_data):
    conll_data = []
    for sentence in annotated_data:
        for word, label in sentence:
            conll_data.append(f"{word} {label}")
        conll_data.append("")
    return conll_data

def write_to_file(annotated_data, file_name):

    with open(file_name, 'w') as f:
        for sentence in annotated_data:
            for word, label in sentence:
                f.write(f"{word} {label}\n")
            f.write("\n")


def process_file(input_filename, output_name):
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
    data = [generate_varied_sentence() for _ in range(1000)]
    all_annotated_data = []
    for sentence, name, company, city, email, phone in data:
        annotated_sentence = annotate_sentence(sentence, name, company, city, email, phone)
        all_annotated_data.append(annotated_sentence)

    write_to_file(all_annotated_data, "ner_train_data_raw.txt")
    process_file("ner_train_data_raw.txt", "ner_train_data_processed.txt")
