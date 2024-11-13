from collections import defaultdict
from pathlib import Path


def is_valid_file(file):
    return file.is_file() and file.name.endswith("txt")

def order_temp_file():
    temp_file = Path('./output.tmp')
    words = temp_file.read_text().split('\n')

    word_ocurrence_dict = defaultdict(list)

    for line in words:
        word = line.split(':')[0]
        if word:
            word_ocurrence_dict[word].append('1')

    word_ocurrence_list = [{"word": word, "occurrences": occurrences} for word, occurrences in word_ocurrence_dict.items()]

    return word_ocurrence_list