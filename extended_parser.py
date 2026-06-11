import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Папка для сохранения базы данных продуктов.
# Согласно правилам (AGENTS.md), папка my_notes предназначена только для пользователя,
# поэтому скрипт сохраняет "сырые" справочные данные в папку raw/diet/diet_database.
OUTPUT_DIR = os.path.join("raw", "diet", "diet_database")

BASE_URL = "https://health-diet.ru/base_of_food/"

# Заголовки, чтобы сайт не принял наш скрипт за бота и не заблокировал соединение
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def clean_filename(name):
    """
    Очищает переданную строку (название продукта) от символов, 
    которые запрещено использовать в именах файлов в ОС Windows и других.
    """
    clean = re.sub(r'[\\/*?:"<>|]', '_', name)
    # Удаляем лишние пробелы по краям
    return clean.strip()

def save_product(name, calories, protein, fat, carbs):
    """
    Формирует markdown-файл продукта с YAML-фронтматером и сохраняет его на диск.
    """
    # Убеждаемся, что целевая папка существует, если нет - создаем
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Формируем имя файла
    filename = clean_filename(name) + ".md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Собираем содержимое файла с нужными свойствами (properties)
    content = f"""---
type: product_db
source: health-diet.ru
calories_100g: {calories}
protein_100g: {protein}
fat_100g: {fat}
carbs_100g: {carbs}
---

# {name}

Данные о продукте автоматически импортированы с сайта Health-Diet.ru.
"""
    # Записываем файл в кодировке UTF-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_category(url):
    """
    Функция обходит страницу по указанному URL, находит таблицу калорийности
    и извлекает Название, Калории, Белки, Жиры и Углеводы для каждого продукта.
    """
    try:
        print(f"Подключение к: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            print(f"[Ошибка] Соединение не установлено! Статус-код: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        tables = soup.find_all('table')
        if not tables:
            print(f"[Внимание] Таблицы не найдены на странице {url}")
            return
        
        table = tables[0]
        tbody = table.find('tbody')
        if not tbody:
            tbody = table
            
        rows = tbody.find_all('tr')
        count = 0
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 5:
                name = cols[0].get_text(strip=True)
                if name.lower() == 'продукт' or not name:
                    continue
                
                calories = cols[1].get_text(strip=True).replace(',', '.')
                protein  = cols[2].get_text(strip=True).replace(',', '.')
                fat      = cols[3].get_text(strip=True).replace(',', '.')
                carbs    = cols[4].get_text(strip=True).replace(',', '.')

                save_product(name, calories, protein, fat, carbs)
                count += 1
                
        print(f"[Успех] Сохранено {count} продуктов.")

    except Exception as e:
        print(f"[Ошибка] Системный сбой при обработке {url}:\n{e}")

def main():
    print("[Старт] Запуск сборщика всех категорий Health-Diet.ru...\n")
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print("[Ошибка] Не удалось загрузить главную страницу базы.")
            return
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        category_urls = set()
        for a in links:
            href = a['href']
            # Нас интересуют ссылки на категории: /base_of_food/food_24507/ и т.д.
            if '/base_of_food/food_' in href:
                full_url = urljoin(BASE_URL, href)
                category_urls.add(full_url)
                
        category_urls = list(category_urls)
        print(f"Найдено категорий: {len(category_urls)}\n")
        
        for url in category_urls:
            parse_category(url)
            
        print("\n[Завершено] Сбор данных завершен! Все продукты сохранены в", OUTPUT_DIR)
        
    except Exception as e:
        print(f"[Ошибка] Системный сбой при получении категорий:\n{e}")

if __name__ == "__main__":
    main()
