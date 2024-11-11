from pathlib import Path
from threading import Thread
from re import search

import file_utils

def map(file: Path, regex: str):
    if file_utils.is_valid_file(file):
        words = file.read_text().replace('\n', ' ').split(' ')
        with Path('./output.tmp').open('a') as output_file:
            for word in words:
                if search(regex, word):
                    output_file.write(f'{word}: "1"\n')

def reduce(word: str, occurrences: list[str]):
    occurrences_count = len(occurrences)
    print({'word': word, 'occurrences': occurrences_count})
    with Path('./final_file.tmp').open('a') as final_file:
        final_file.write(f'{word}: {occurrences_count}\n')

if __name__ == '__main__':
    regex = input("Informe o regex: ")

    path = Path('./')
    files_on_path = path.glob('*')

    map_threads = []

    # Executa a função map em uma thread para cada arquivo
    for file in files_on_path:
        thread = Thread(target=map, args=(file, regex,))
        thread.start()
        map_threads.append(thread)

    # Aguarda todas as threads do map terminarem antes de chamar a função reduce
    for thread in map_threads:
        thread.join()

    # Ordena o arquivo temporário e obtém a lista de ocorrências de palavras
    word_ocurrence_list = file_utils.order_temp_file()

    reduce_threads = []

    # Executa a função em uma Thread para cada palavra junto de suas ocorrências
    for word_ocurrence in word_ocurrence_list:
        word = word_ocurrence.get('word')
        occurrences = word_ocurrence.get('occurrences')
        thread = Thread(target=reduce, args=(word, occurrences))
        thread.start()
        reduce_threads.append(thread)

    for thread in reduce_threads:
        thread.join()