import requests
from collections import defaultdict
from math import log

# Читаем текстовый файл по url-ссылке
data = requests.get("https://raw.githubusercontent.com/SkillfactoryDS/Datasets/master/war_peace_processed.txt").text

# Предобрабатываем текстовый файл
data = data.split('\n')
data.remove('')
data = data + ['[new chapter]']

# Разделим текст на главы
chapter_data = []
chapter_words_count = []

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

# Функция для вычисления DF для заданного слова
def get_df(word):
    # Считаем количество глав, в которых встречается это слово
    count_docs = 0
    for chapter_dict in chapter_words_count:
        if word in chapter_dict:
            count_docs += 1
    # Общее количество глав
    total_docs = len(chapter_words_count)
    # Рассчитываем DF
    return count_docs / total_docs

# Функция для получения DF для всех уникальных слов
def compute_all_df():
    df_dict = defaultdict(float)
    # Собираем все уникальные слова
    unique_words = set(word for chapter in chapter_data for word in chapter)
    # Для каждого слова вычисляем DF
    for word in unique_words:
        df_dict[word] = get_df(word)
    return df_dict

# Функция для вычисления tf-idf для заданного слова в заданной главе
def compute_tf_idf(word, chapter_number):
    # Получаем частоту термина в указанной главе
    chapter_word_count = chapter_words_count[chapter_number]
    tf = chapter_word_count.get(word, 0) / len(chapter_data[chapter_number])
    
    # Получаем DF для слова
    df = get_df(word)
    if df == 0:  # Чтобы избежать деления на ноль
        return 0
    
    # Рассчитываем IDF
    idf = 1 / df
    
    # Вычисляем tf-idf
    tf_idf = tf * log(idf)
    return tf_idf

# Функция для нахождения трех слов с наибольшим tf-idf в главе
def top_3_tf_idf(chapter_number):
    tf_idf_dict = {}
    # Получаем все уникальные слова в указанной главе
    chapter_words = set(chapter_data[chapter_number])
    for word in chapter_words:
        tf_idf_dict[word] = compute_tf_idf(word, chapter_number)
    
    # Сортируем слова по tf-idf в порядке убывания
    sorted_tf_idf = sorted(tf_idf_dict.items(), key=lambda item: item[1], reverse=True)
    
    # Выводим топ-3 слова
    top_3 = sorted_tf_idf[:3]
    return top_3

# Пример: Выводим топ-3 слова для 3-й главы
target_chapter = 3
top_3_words = top_3_tf_idf(target_chapter)

print(f"Топ-3 слова для главы {target_chapter} с наибольшим tf-idf:")
for word, tf_idf in top_3_words:
    print(f"Слово: {word}, TF-IDF: {tf_idf:.6f}")
