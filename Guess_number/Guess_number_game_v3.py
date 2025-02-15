"""Игра угадай число
Компьютер сам загадывает и сам угадывает число
"""

import numpy as np

def game_core_v3(number: int = 1) -> int:
    """Угадываем число с помощью бинарного (двоичного) поиска."""
    count = 0
    low, high = 1, 100
    
    while low <= high:
        count += 1
        mid = (low + high) // 2  # Находим середину диапазона
        
        if mid == number:
            return count  # Число угадано
        elif mid < number:
            low = mid + 1  # Ищем в правой половине
        else:
            high = mid - 1  # Ищем в левой половине
    
    return count

def score_game(predict_function) -> int:
    """Оцениваем среднее количество попыток угадывания на 1000 числах."""
    count_ls = []
    np.random.seed(1)  # Фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=1000)  # Генерируем 1000 случайных чисел
    
    for number in random_array:
        count_ls.append(predict_function(number))
    
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score

if __name__ == "__main__":
    score_game(game_core_v3)