import requests
from collections import defaultdict

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

# Пример: вычислим DF для слова "человек"
target_word = 'человек'

df_result = get_df(target_word)
print(f"Document Frequency для слова '{target_word}': {df_result:.4f}")

# Пример: вычислим DF для всех уникальных слов
df_all = compute_all_df()
# Выведем DF для первых 10 слов (для теста)
for i, (word, df) in enumerate(df_all.items()):
    if i == 10:
        break
    print(f"DF для слова '{word}': {df:.4f}")
