import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает данные из JSON-файла. Если файла нет, возвращает пустой словарь {}."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
            
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    """Сохраняет переданные данные в JSON-файл, если он существует. 
    Если не существует, создаст новый и запишет."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """Загружает данные таблицы из файла. Если файла нет — возвращает []."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохраняет переданные данные таблицы в JSON-файл, если он существует. 
    Если не существует, создаст новый и запишет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)