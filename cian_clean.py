import re
import numpy as np
import pandas as pd

df = pd.read_csv('cian_row.csv', delimiter=';', encoding='utf-8')
print(f"Успешно! Прочитано строк: {len(df)}")
list_of_columns = df.columns.tolist()

# Удаляем ненужные столбцы
df = df.iloc[1:].reset_index(drop=True)
df.drop(columns='Unnamed: 0', inplace=True)
df.drop(columns='Unnamed: 1', inplace=True)
df.drop(columns='Unnamed: 9', inplace=True)
df.drop(columns='Unnamed: 10', inplace=True)
df.drop(columns='Unnamed: 15', inplace=True)
df.drop(columns='Unnamed: 20', inplace=True)
df.drop(columns='Unnamed: 21', inplace=True)
df.drop(columns='Unnamed: 22', inplace=True)
df.drop(columns='Unnamed: 28', inplace=True)
df.drop(columns='Unnamed: 35', inplace=True)

# Приводим в порядок ячейки
link_pattern = r'🔗\s*https?://[^\s]+|https?://[^\s]+'
symbol_pattern = r'\n✏️'

for column in df.columns:
    if df[column].dtype == 'object':
        # Сначала удаляем ссылки и заменяем на NaN
        mask = df[column].astype(str).str.contains(link_pattern, regex=True)
        df.loc[mask, column] = np.nan

        # Удаляем \n✏️ из оставшихся ячеек
        df[column] = df[column].str.replace(symbol_pattern, '', regex=True)

        # Заменить Empty на Nan
        empty_mask = df[column].astype(str).str.strip().str.lower() == 'empty'
        df.loc[empty_mask, column] = np.nan

# Удаляем столбцы с более чем 50% NaN
initial_columns = len(df.columns)
threshold = len(df) * 0.5
df = df.dropna(axis=1, thresh=threshold)  # Изменено: работаем с df вместо df_cleaned
print(f"Было столбцов: {initial_columns}")
print(f"Стало столбцов: {len(df.columns)}")

# Разбиваем поле с информацией 2-комн. квартира, 36,77 м², 4/31 этаж на отдельные поля
def parse_apartment_info(text):
    """
    Парсит строку с информацией о квартире
    """
    if pd.isna(text):
        return pd.Series([None, None, None, None])

    text = str(text).strip()

    # Инициализируем значения по умолчанию
    rooms = None
    area = None
    floor = None
    total_floors = None

    # Парсим количество комнат
    room_match = re.search(r'(\d+)-комн\.|Студия', text)
    if room_match:
        if room_match.group(0) == 'Студия':
            rooms = 1
        else:
            rooms = int(room_match.group(1))

    # Парсим площадь
    area_match = re.search(r'(\d+[,.]\d+)\s*м²', text)
    if area_match:
        area_str = area_match.group(1).replace(',', '.')
        area = float(area_str)

    # Парсим этажи
    floor_match = re.search(r'(\d+)/(\d+)\s*этаж', text)
    if floor_match:
        floor = int(floor_match.group(1))
        total_floors = int(floor_match.group(2))

    return pd.Series([rooms, area, floor, total_floors])

# Применяем функцию к столбцу
new_columns = df.pop('Unnamed: 2').apply(parse_apartment_info)
new_columns.columns = ['Комнаты', 'Площадь', 'Этаж', 'Этажность']

# Вставляем новые столбцы в начало
for i, col_name in enumerate(['Комнаты', 'Площадь', 'Этаж', 'Этажность']):
    df.insert(i, col_name, new_columns[col_name])

# Достаем цену за кв метр
def extract_price(text):
    if pd.isna(text):
        return None
    text = str(text)
    # Ищем число с пробелами и символами валюты
    match = re.search(r'(\d[\d\s]*[\d,])\s*₽', text)
    if match:
        # Убираем пробелы и заменяем запятую на точку (если есть)
        price_str = match.group(1).replace(' ', '').replace(',', '.')
        return int(price_str)
    return None

df['Цена за м²'] = df['Unnamed: 17'].apply(extract_price)
df.drop(columns='Unnamed: 17', inplace=True)

# Переименуем столбцы
df.rename(columns={'Unnamed: 3': 'Информация по срокам сдачи'}, inplace=True)
df.rename(columns={'Unnamed: 4': 'Ипотека и скадки'}, inplace=True)
df.rename(columns={'Unnamed: 5': 'Наименование ЖК'}, inplace=True)
df.rename(columns={'Unnamed: 8': 'Станция метро'}, inplace=True)
df.rename(columns={'Unnamed: 11': 'Район'}, inplace=True)
df.rename(columns={'Unnamed: 13': 'Микрорайон'}, inplace=True)

df.rename(columns={'Unnamed: 19': 'Зайстройщик'}, inplace=True)
df.rename(columns={'Unnamed: 40': 'Осталось квартир'}, inplace=True)
# Смотрим что вышло в итоге
pd.set_option('display.max_columns', None)
print(df.head(20))

# Сохраняем в новый файл
df.to_csv('cian_clean.csv', index=False, sep=';', encoding='utf-8')