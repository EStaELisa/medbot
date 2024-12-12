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
        f"{name} is a patient at {company} in {city}. Contact them at {email} or {phone}.",
        f"Dr. {name} works at {company} located in {city}. You can reach the doctor at {email} or {phone}.",
        f"{name} is scheduled for an appointment at {company} in {city}. For inquiries, call {phone} or email {email}.",
        f"To discuss your test results, contact {name} at {company} in {city} via {email} or {phone}.",
        f"Reach out to {name} at {company} in {city} for medical advice. Email: {email}, Phone: {phone}.",
        f"{name} from {company} in {city} is available for consultation at {email} or {phone}.",
        f"Patient {name} can be contacted through {company} in {city} at {email} or {phone}.",
        f"For further assistance, email {name} at {email} in {city} or call {phone}.",
        f"{name}'s medical records are at {company} in {city}. Contact: {email}, {phone}.",
        f"{name} has an appointment at {company} in {city}. Confirm via {email} or call {phone}.",
        f"Please reach {name} at {company} in {city} for health concerns. Email: {email}, Phone: {phone}.",
        f"{name} from {company} in {city} can be contacted at {email} or {phone} for follow-up.",
        f"Your next visit with {name} at {company} in {city} is scheduled. Contact: {email}, {phone}.",
        f"Dr. {name} from {company} in {city} is available at {email} or {phone} for consultation.",
        f"{name}'s records at {company} in {city} can be accessed through {email} or {phone}.",
        f"To reschedule, contact {name} at {company} in {city} via {email} or {phone}.",
        f"Reach out to {name} at {company} in {city} for test results. Email: {email}, Phone: {phone}.",
        f"For any medical inquiries, contact {name} at {company} in {city} via {email} or {phone}.",
    ]
    sentence = random.choice(templates)
    return sentence, name, company, city, email, phone


def prepare_sentence(sentence):
    s = sentence[:-1]
    s = s.replace(",", " ")
    words = s.split()
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


if __name__ == "__main__":
    data = [generate_varied_sentence() for _ in range(10)]
    annotated_data = []
    for sentence, name, company, city, email, phone in data:
        annotated_sentence = annotate_sentence(sentence, name, company, city, email, phone)
        annotated_data.append(annotated_sentence)

    write_to_file(annotated_data, "ner_train_data.txt")