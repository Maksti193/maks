import os
import json
import re
from datetime import datetime

def convert_dates_in_file(file_path):
    """Convert dates in a single JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла: {file_path}")
            return

    # Функция для рекурсивного обхода структуры JSON
    def process_item(item):
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    # Проверяем, соответствует ли строка формату даты yyyy-mm-dd 00:00:00
                    match = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2}) 00:00:00', value)
                    if match:
                        # Преобразуем в новый формат
                        year, month, day = match.groups()
                        item[key] = f"{day}.{month}.{year}"
                else:
                    process_item(value)
        elif isinstance(item, list):
            for element in item:
                process_item(element)

    process_item(data)

    # Сохраняем изменения обратно в файл
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_directory(directory):
    """Process all JSON files in directory and subdirectories"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Обработка файла: {file_path}")
                convert_dates_in_file(file_path)

if __name__ == '__main__':
    target_directory = input("Введите путь к директории с JSON файлами: ")
    if os.path.isdir(target_directory):
        process_directory(target_directory)
        print("Обработка завершена!")
    else:
        print("Указанная директория не существует")