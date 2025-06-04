from string import punctuation
from prescription_db import *

from nltk import word_tokenize, corpus
from nltk.corpus import floresta

PRESCRIPTIONS = os.getcwd() + '/Receituarios'
PRESCRIPTIONS_QUANTITY = 7

LANGUAGE = "portuguese"
UNWANTED_GRAMMATICAL_CLASSES = [
    "adv",
    "num",
    "v-inf",
    "v-fin",
    "v-pcp",
    "v-ger",
    "adj",
    "pron",
    "n",
    "proun",
    "v"
]

def init():
    stop_words = set(corpus.stopwords.words(LANGUAGE))
    classifications = {}
    for (word, classification) in floresta.tagged_words():
        classifications[word.lower()] = classification

    return stop_words, classifications

def read_prescriptions(prescription):
    success, content = False, None
    try:
        with open(prescription, "r") as file:
            content = file.read()
            file.close()
        success = True
    except Exception as e:
        print(f"Error ao ler o receituário: {str(e)}")

    return success, content

def extract_title(prescription_content):
    marker = "Receita:"
    marker = prescription_content.index(marker) + len(marker)

    title = prescription_content[marker:]
    title = title[:title.index("\n")]

    return title

def remove_title_from_prescription(title, prescription_content):
    marker = prescription_content.index(title) + len(title)

    content = prescription_content[marker:]

    return content

def remove_stop_words(tokens, stop_words):
    filtered_tokens = []
    for token in tokens:
        if token.lower() not in stop_words:
            filtered_tokens.append(token)

    return filtered_tokens

def remove_unwanted_grammatical_classes(tokens, classifications):
    filtered_tokens = []
    for token in tokens:
        if token.lower() not in classifications.keys():
            filtered_tokens.append(token)
            continue
        classification = classifications[token.lower()]
        if not any (s in classification for s in UNWANTED_GRAMMATICAL_CLASSES):
            filtered_tokens.append(token)

    return filtered_tokens

def remove_punctuation(tokens):
    filtered_tokens = []
    for token in tokens:
        if token not in punctuation:
            filtered_tokens.append(token)

    return filtered_tokens

if __name__ == "__main__":
    stop_words, classifications = init()
    init_prescription_db()

    print("Processando prescrições...")
    for count in range(1, PRESCRIPTIONS_QUANTITY):
        prescription = f"{PRESCRIPTIONS}/{count}.txt"
        file_name = f"{count}.txt"
        success, prescription_content = read_prescriptions(prescription)
        if success:
            prescription_title = extract_title(prescription_content)
            prescription_content = remove_title_from_prescription(prescription_title, prescription_content)

            prescription_tokens = word_tokenize(prescription_content)
            prescription_tokens = remove_stop_words(prescription_tokens, stop_words)
            prescription_tokens = remove_unwanted_grammatical_classes(prescription_tokens, classifications)
            prescription_tokens = remove_punctuation(prescription_tokens)

            success, message = generate_prescription(count, prescription_title, file_name, prescription_tokens)
            if success is False:
                print(f"{message}")

    print("Processamento finalizado")