import pandas as pd
import json
import re

# Загрузка данных из таблицы товаров
store_df = pd.read_excel('store.xlsx')  
suppliers_df = pd.read_excel('suppliers.xlsx')  

# Список слов для исключения
excluded_words = ['планшет', 'apple', 'смартфон', 'nano sim', 'esim', 'dualsim', 'huawei']

# Функция для токенизации названия товара с исключением слов
def tokenize_product_name(product_name):
    if isinstance(product_name, str):  # Проверяем, что product_name строка
        cleaned_name = product_name.lower()  
        cleaned_name = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9\s/+\-]', '', cleaned_name)  # Убираем спец символы
        tokens = cleaned_name.split()  # Разбиваем строку на токены
        tokens = [token for token in tokens if token not in excluded_words]
        return tokens
    else:
        return []  


store_products_dict = {}
for index, row in store_df.iterrows():
    product_name = row['Наименование']  
    store_products_dict[product_name] = tokenize_product_name(product_name)

# Создание списка для товаров поставщиков
suppliers_products_list = []
for index, row in suppliers_df.iterrows():
    supplier_name = row['поставщик']  
    supplier_product_name = row['прайс'] 
    tokens = tokenize_product_name(supplier_product_name)
    
    suppliers_products_list.append({
        "поставщик": supplier_name,
        "название": supplier_product_name,
        "токены": tokens
    })

# Сохранение словарей в JSON
with open('store_products.json', 'w', encoding='utf-8') as store_json_file:
    json.dump(store_products_dict, store_json_file, ensure_ascii=False, indent=4)

with open('suppliers_products.json', 'w', encoding='utf-8') as suppliers_json_file:
    json.dump(suppliers_products_list, suppliers_json_file, ensure_ascii=False, indent=4)

print("Словари товаров сохранены.")