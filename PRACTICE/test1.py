import requests
import re
from collections import defaultdict

# Читаем текстовый файл по url-ссылке
data = requests.get("https://raw.githubusercontent.com/SkillfactoryDS/Datasets/master/war_peace_processed.txt").text

# Предобрабатываем текстовый файл
data = data.split('\n')
data.remove('')
data = data + ['[new chapter]']

# Разделим текст на главы и подсчитаем количество слов в каждой главе
chapter_data = []
chapter_words_count = []

# Инициализируем список для слов в главе
chapter_words = []

# Создаем цикл по всем словам
for word in data:
    if word == '[new chapter]':
        chapter_data.append(chapter_words)  # Добавляем текущую главу
        chapter_words = []  # Перезапускаем список для следующей главы
    else:
        chapter_words.append(word)

# Подсчитываем частоту каждого слова в каждой главе
for chapter_words in chapter_data:
    temp = defaultdict(int)
    for word in chapter_words:
        temp[word] += 1
    chapter_words_count.append(temp)

# Функция для вычисления TF для заданного слова в заданной главе
def get_tf(word, chapter_index):
    # Получаем количество слов в главе
    total_words_in_chapter = sum(chapter_words_count[chapter_index].values())
    # Получаем количество вхождений слова в главу
    word_count_in_chapter = chapter_words_count[chapter_index].get(word, 0)
    # Рассчитываем TF
    if total_words_in_chapter == 0:
        return 0
    return word_count_in_chapter / total_words_in_chapter

# Пример: вычислим TF для слова "князю" в 15-й главе
target_word = 'князю'
target_chapter = 15

tf_result = get_tf(target_word, target_chapter)
print(f"Частота слова '{target_word}' в главе {target_chapter}: {tf_result:.6f}")