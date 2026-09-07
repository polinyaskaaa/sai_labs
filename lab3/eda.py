import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "lab3_shi.csv"
df = pd.read_csv(DATA_PATH)

# початковий перегляд датасету
print("Перші 5 рядків набору даних:")
print(df.head())
print("Розмір набору даних:")
print("Кількість записів:", df.shape[0])
print("Кількість колонок:", df.shape[1])

# загальна інформація про структуру даних
print("\nІнформація про набір даних:")
df.info()

# типи даних
print("\nТипи даних:")
print(df.dtypes)

categorical_columns = [
    "airline",
    "flight",
    "source_city",
    "departure_time",
    "stops",
    "arrival_time",
    "destination_city",
    "class"
]

numeric_columns = [
    "duration",
    "days_left",
    "price"
]

print("\nКатегоріальні ознаки:")
print(categorical_columns)

print("\nЧислові ознаки:")
print(numeric_columns)

# пропущені значення
print("\nКількість пропущених значень у кожній колонці:")
print(df.isnull().sum())

print("\nЗагальна кількість пропущених значень:")
print(df.isnull().sum().sum())

# числові характеристики
print("\nСтатистичні характеристики числових ознак:")
print(df[["duration", "days_left", "price"]].describe())


# цільова змінна
print("\nСтатистичні характеристики цільової змінної price:")
print(df["price"].describe())

# гістограма розподілу ціни
plt.figure(figsize=(9, 5))
plt.hist(df["price"], bins=50)
plt.title("Розподіл вартості авіаквитків")
plt.xlabel("Вартість авіаквитка")
plt.ylabel("Кількість записів")
plt.show()

# boxplot цільової змінної
plt.figure(figsize=(9, 4))
plt.boxplot(df["price"], vert=False)
plt.title("Розподіл вартості авіаквитків")
plt.xlabel("Вартість авіаквитка")
plt.show()


# ціна залежно від класу
print("\nСтатистика ціни за класом квитка:")
price_by_class = df.groupby("class")["price"].agg(
    ["count", "mean", "median", "min", "max"]
)
print(price_by_class)

# перевірка логічності допустимих значень
print("\nПеревірка некоректних значень:")

print(
    "Кількість записів з ціною <= 0:",
    (df["price"] <= 0).sum()
)

print(
    "Кількість записів з тривалістю польоту <= 0:",
    (df["duration"] <= 0).sum()
)

print(
    "Кількість записів з days_left < 0:",
    (df["days_left"] < 0).sum()
)

print(
    "Кількість записів, де місто відправлення "
    "і місто призначення однакові:",
    (df["source_city"] == df["destination_city"]).sum()
)


# дублікати
print("\nКількість повністю однакових записів:")
print(df.duplicated().sum())


# унікальні значення категоріальних ознак
print("\nУнікальні значення категоріальних ознак:")

columns_to_check = [
    "airline",
    "source_city",
    "departure_time",
    "stops",
    "arrival_time",
    "destination_city",
    "class"
]

for column in columns_to_check:
    print(f"\n{column}:")
    print(df[column].unique())

print("\nКількість унікальних значень:")
print(df.nunique())


# викиди
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["price"] < lower_bound) |
    (df["price"] > upper_bound)
]

print("\nАналіз можливих викидів у price:")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Нижня межа:", lower_bound)
print("Верхня межа:", upper_bound)
print("Кількість можливих викидів:", len(outliers))


# найдорожчі авіаквитки
print("\n10 найдорожчих авіаквитків:")

print(
    df.sort_values(
        by="price",
        ascending=False
    ).head(10)
)