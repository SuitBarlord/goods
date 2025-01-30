import pandas as pd
import json
import re
from difflib import SequenceMatcher

# Загрузка данных из таблицы
store_df = pd.read_excel('store.xlsx')
suppliers_df = pd.read_excel('suppliers.xlsx')

# Список допустимых цветов
colors = ['черный', 'белый', 'красный', 'синий', 'зеленый', 'желтый', 'серый', 'пурпурный', 'розовый', 'голубой']

# Список стоп-слов
stop_words = ['смартфон', 'планшет', 'apple']

# Функция для токенизации названия товара
def tokenize_product_name(product_name):
    if isinstance(product_name, str):
        cleaned_name = product_name.lower()
        cleaned_name = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9\s/+\-]', '', cleaned_name)
        tokens = cleaned_name.split()
        # Убираем стоп-слова
        tokens = [token for token in tokens if token not in stop_words]
        return set(tokens)
    return set()

# Функция для извлечения цвета
def extract_color(product_name):
    if isinstance(product_name, str):
        product_name = product_name.lower()
        for color in colors:
            if color in product_name:
                return color
    return None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Создание словаря для товаров
store_products_dict = {}
for index, row in store_df.iterrows():
    product_name = row['Наименование']
    store_products_dict[product_name] = {
        'tokens': tokenize_product_name(product_name),
        'color': extract_color(product_name)
    }

# Список для товаров поставщиков
suppliers_products_list = []
for index, row in suppliers_df.iterrows():
    supplier_name = row['поставщик']
    supplier_product_name = row['прайс']
    tokens = tokenize_product_name(supplier_product_name)

    suppliers_products_list.append({
        "поставщик": supplier_name,
        "название": supplier_product_name,
        "tokens": tokens,
        "color": extract_color(supplier_product_name)
    })

# Сопоставление товаров из магазина с товарами поставщиков
matches = {}
for store_product, store_info in store_products_dict.items():
    matches[store_product] = []
    for supplier_product in suppliers_products_list:
        supplier_tokens = supplier_product['tokens']
        token_intersection = store_info['tokens'].intersection(supplier_tokens)

        colors_match = (store_info['color'] == supplier_product['color'])

        # Проверка на совпадение токенов
        if len(token_intersection) > 0 and colors_match:
            similarity_score = similar(store_product, supplier_product['название'])
            if similarity_score > 0.42:  # Установленный порог схожести
                matches[store_product].append({
                    "поставщик": supplier_product['поставщик'],
                    "название": supplier_product['название'],
                    "сходство": similarity_score,
                    "цвет": supplier_product['color']
                })

# Сохранение совпадений в JSON файл
with open('matches.json', 'w', encoding='utf-8') as matches_json_file:
    json.dump(matches, matches_json_file, ensure_ascii=False, indent=4)

print("Сопоставления товаров сохранены в 'matches.json'.")


