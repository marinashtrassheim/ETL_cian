import re
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('cian_clean.csv', delimiter=';', encoding='utf-8')
print(f"Успешно! Прочитано строк: {len(df)}")
print(df.head())
list_of_columns = df.columns.tolist()

print("=" * 60)
print("ОПИСАНИЕ НАБОРА ДАННЫХ")
print("=" * 60)

# Кол-во строк и столбцов
print(f"Размер данных: {df.shape[0]} строк, {df.shape[1]} столбцов")

# Создаем DataFrame с информацией о столбцах
column_info = pd.DataFrame({
    'Тип данных': df.dtypes,
    'Не нулевые': df.count(),
    'Пропуски': df.isnull().sum(),
    '% Пропусков': (df.isnull().sum() / len(df) * 100).round(2)
})

print(column_info)

# Средняя цена по районам
price_by_district = df.groupby('Район')['Цена за м²'].mean().sort_values(ascending=False)

print("СРЕДНЯЯ ЦЕНА ЗА М² ПО РАЙОНАМ:")
print("=" * 40)
for district, price in price_by_district.items():
    print(f"{district}: {price:,.0f} ₽/м²")

# Визуализация
plt.figure(figsize=(10, 6))
price_by_district.plot(kind='bar')
plt.title('Средняя цена за м² по районам')
plt.ylabel('Цена за м², руб')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Корреляция между площадью и ценой
correlation = df['Площадь'].corr(df['Цена за м²'])
print(f"\nКОРРЕЛЯЦИЯ ПЛОЩАДЬ-ЦЕНА: {correlation:.2f}")

# Визуализация
plt.figure(figsize=(8, 6))
plt.scatter(df['Площадь'], df['Цена за м²'], alpha=0.6)
plt.xlabel('Площадь, м²')
plt.ylabel('Цена за м², руб')
plt.title('Зависимость цены от площади')
plt.show()

# Средняя цена по количеству комнат
price_by_rooms = df.groupby('Комнаты')['Цена за м²'].mean()

print("\nСРЕДНЯЯ ЦЕНА ПО КОЛИЧЕСТВУ КОМНАТ:")
print("=" * 35)
for rooms, price in price_by_rooms.items():
    print(f"{rooms:.0f}-комн.: {price:,.0f} ₽/м²")

# Визуализация
plt.figure(figsize=(8, 6))
price_by_rooms.plot(kind='bar')
plt.title('Средняя цена за м² по количеству комнат')
plt.ylabel('Цена за м², руб')
plt.xlabel('Количество комнат')
plt.show()

# Средняя цена по микрорайонам (топ-10)
price_by_microdistrict = df.groupby('Микрорайон')['Цена за м²'].mean().sort_values(ascending=False).head(10)

print("\nТОП-10 МИКРОРАЙОНОВ ПО ЦЕНЕ:")
print("=" * 35)
for microdistrict, price in price_by_microdistrict.items():
    print(f"{microdistrict}: {price:,.0f} ₽/м²")

# Средняя этажность по районам
floors_by_district = df.groupby('Район')['Этажность'].mean().sort_values(ascending=False)

print("\nСРЕДНЯЯ ЭТАЖНОСТЬ ПО РАЙОНАМ:")
print("=" * 35)
for district, floors in floors_by_district.items():
    print(f"{district}: {floors:.1f} этажей")

