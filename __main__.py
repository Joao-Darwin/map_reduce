from pathlib import Path
from threading import Thread

import file_utils

def map(file: Path):
    if file_utils.is_valid_file(file):
        words = file.read_text().replace('\n', ' ').split(' ')
        with Path('./output.tmp').open('a') as output_file:
            for word in words:
                output_file.write(f'{word}: "1"\n')

def reduce(word: str, occurrences: list[str]):
    occurrences_count = len(occurrences)
    print({'word': word, 'occurrences': occurrences_count})

if __name__ == '__main__':
    path = Path('./')
    files_on_path = path.glob('*')

    map_threads = []

    # Executa a função map em uma thread para cada arquivo
    for file in files_on_path:
        thread = Thread(target=map, args=(file,))
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