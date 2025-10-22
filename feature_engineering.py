import pandas as pd

df = pd.read_csv('cian_clean.csv', delimiter=';', encoding='utf-8')
print(f"Успешно! Прочитано строк: {len(df)}")

# Создадим рейтинг застройщика, основанный на средней стоимости за квадратный метр

df['Рейтинг застройщика'] = (
    df.groupby('Зайстройщик')['Цена за м²']
    .transform('mean')
    .fillna(0)  # Заменяем NaN на 0
    .rank(method='dense', ascending=False)
    .astype(int)
)

print(df.head(30))