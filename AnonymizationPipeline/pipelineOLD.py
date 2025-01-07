# TODO: welche Module uebernehmen?

from typing import List
import anonymize  # Anonymisierungsmethoden für sensible Daten
import ingestors  # Eingabeformate und Verarbeitung
from sensitive_identification.name_identifiers import RoBERTaNameIdentifier, \
    SpacyIdentifier  # Modelle für Named Entity Recognition (NER)
from sensitive_identification.regex_identification import RegexIdentifier  # Regex-basierte Erkennung sensibler Daten
import configargparse  # Zum Einlesen von Konfigurationsdateien und Kommandozeilenargumenten
from tqdm import tqdm  # Fortschrittsbalken für lange Operationen
from copy import deepcopy  # Zum Erstellen von Kopien, um Daten vor Veränderungen zu schützen

# Modul für die Erkennung sensibler Daten
from sensitive_identification.sensitive_identifier import SensitiveIdentifier
# TrueCaser korrigiert Groß- und Kleinschreibung im Text
from truecaser.TrueCaser import TrueCaser

# Initialisierung des TrueCasers
tc = TrueCaser('truecaser/english.dist')


# Funktion, um eine Liste von Labels (z. B. "PERSON", "DATE") aus einer Datei zu laden
def get_labels(path: str) -> List[str]:
    label_list: List[str] = []
    with open(path, "r") as f:
        for line in f:
            label_list.append(line.strip())  # Jede Zeile der Datei wird als Label hinzugefügt
    return label_list


# Hauptfunktion der Pipeline
def main():
    # Parser für Kommandozeilenargumente und Konfigurationsdateien
    parser = configargparse.ArgumentParser(
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
        default_config_files=['./*conf']  # Standardmäßige Konfigurationsdateien
    )
    # Hinzufügen der verfügbaren Argumente
    parser.add('-c', '--config', required=False, is_config_file=True, help='Pfad zur Konfigurationsdatei')
    parser.add_argument("-i", "--input", type=str, required=True, help="Eingabedatei mit Texten")
    parser.add_argument("-m", "--models", type=str, nargs="*", default=["es_anonimization_core_lg", "xx_ent_wiki_sm"],
                        help="Liste der NER-Modelle")
    parser.add_argument("-t", "--type_of_models", nargs="*", choices=["spacy", "huggingface"],
                        default=["spacy", "spacy"],
                        help="Typ der NER-Modelle (Spacy oder Huggingface)")
    parser.add_argument("-f", "--format", choices=["plain", "jsonl", "doccano"], default="plain",
                        help="Format der Eingabedatei")
    parser.add_argument("-a", "--anonym_method", choices=["label", "random", "intelligent", "none"], default="none",
                        help="Art der Anonymisierung")
    parser.add_argument("-o", "--output", type=str, default="output/output.txt", help="Pfad zur Ausgabedatei")
    parser.add_argument("-l", "--labels", type=str, help="Datei mit einer Liste von Labels für NER-Modelle")
    parser.add_argument("-r", "--regexes", type=str, default="data/regex_definition.csv",
                        help="CSV-Datei mit Regex-Definitionen für die Erkennung")

    # Einlesen der Argumente
    args = parser.parse_args()

    # Zuweisung der Argumente zu Variablen
    input_path: str = args.input  # Eingabedatei mit Texten
    output_path: str = args.output  # Ausgabedatei
    model_paths: List[str] = args.models  # Pfade zu den NER-Modellen
    model_types: List[str] = args.type_of_models  # Typ der NER-Modelle
    input_format: str = args.format  # Eingabeformat (plain, JSONL oder Doccano)
    anonym_method: str = args.anonym_method  # Anonymisierungsmethode
    labels: str = args.labels  # Datei mit Labels
    regex_definitions: str = args.regexes  # Datei mit Regex-Definitionen

    # Sicherstellen, dass die Anzahl der Modelle und Typen übereinstimmt
    assert len(model_paths) == len(model_types), "Die Anzahl der Modelle und Typen muss übereinstimmen"

    # Falls Labels angegeben wurden, werden sie eingelesen
    label_list = None
    if labels:
        label_list = get_labels(labels)

    # NER-Modelle initialisieren
    ner_models: List[SensitiveIdentifier] = []
    print("Laden der Modelle")
    for model_path, model_type in zip(model_paths, model_types):
        if model_type == "spacy":
            ner_models.append(SpacyIdentifier(model_path, label_list))  # Spacy-Modelle laden
        else:
            ner_models.append(RoBERTaNameIdentifier(model_path, label_list))  # Huggingface-Modelle laden
    print("Modelle erfolgreich geladen")

    # Eingabedatei basierend auf dem Format verarbeiten
    if input_format == "plain":
        ingestor = ingestors.PlainTextingestor(input_path)
    elif input_format == "jsonl":
        ingestor = ingestors.Prodigyingestor(input_path)
    else:
        ingestor = ingestors.Doccanoingestor(input_path)

    # Regex-basierte Erkennung initialisieren
    regex_identifier = RegexIdentifier(regex_definitions, label_list)

    # Verarbeitung der Registries (Texte)
    for reg in tqdm(ingestor.registries, "Erkennung sensibler Daten"):
        original_reg = deepcopy(reg)  # Originaltext sichern
        reg.text = tc.get_true_case(reg.text)  # Groß- und Kleinschreibung korrigieren
        regex_identifier.identify_sensitive(reg)  # Regex-Erkennung ausführen
        for ner_model in ner_models:
            ner_model.identify_sensitive(reg)  # NER-Modelle anwenden
        reg.text = original_reg.text  # Text zurücksetzen

    # Falls Anonymisierung gewählt wurde
    if anonym_method != "none":
        print("Anonymisierer wird instanziiert")
        if anonym_method == "label":
            anonymizer = anonymize.LabelAnonym()
        elif anonym_method == "random":
            anonymizer = anonymize.RandomAnonym()
        else:
            anonymizer = anonymize.AllAnonym()
        ingestor.anonymize_registries(anonymizer)  # Anonymisierung ausführen

    # Ergebnisse speichern
    ingestor.save(output_path)


# Einstiegspunkt für die Ausführung des Programms
if __name__ == "__main__":
    main()