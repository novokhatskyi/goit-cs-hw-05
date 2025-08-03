from rich import print
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import string
from time import time
from vizualization import draw_diagram_by_words


def read_text(url):
    responce= urllib.request.urlopen(url)
    data = responce.read()
    # print (data.decode('utf-8'))
    return data.decode('utf-8')

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()
    words = [word for word in words if len(word) > 2]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)





if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    start = time()
    text = read_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        search_words = ['war', 'peace', 'love']
        result = map_reduce(text)
        top_12 = sorted(result.items(), key=lambda x: x[1], reverse=True)[:12]
        print("Результат підрахунку слів:", top_12)
        print(f"Загальний час виконання коду: {time() - start:.2f} секунд")
         # Підготовка даних для графіка
        words = [pair[0] for pair in top_12]
        counts = [pair[1] for pair in top_12]

        # Побудова діаграми
        draw_diagram_by_words(words, counts, title="12 найбільш уживаних слів")
        
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
    
