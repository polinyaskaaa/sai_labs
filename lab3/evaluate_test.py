from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import train_test_split
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ============================================================
# НАЛАШТУВАННЯ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "lab3_shi.csv"

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "random_forest.joblib"
)

RANDOM_STATE = 42


CATEGORICAL_COLUMNS = [
    "airline",
    "source_city",
    "departure_time",
    "stops",
    "arrival_time",
    "destination_city",
    "class",
]

NUMERIC_COLUMNS = [
    "duration",
    "days_left"
]

FEATURE_COLUMNS = (
    CATEGORICAL_COLUMNS
    + NUMERIC_COLUMNS
)


# ============================================================
# ЗАВАНТАЖЕННЯ ДАТАСЕТУ
# ============================================================

df = pd.read_csv(
    DATASET_PATH
)


# Видаляємо ті самі стовпці,
# що і під час навчання
df = df.drop(
    columns=[
        "Unnamed: 0",
        "flight"
    ],
    errors="ignore"
)


X = df[
    FEATURE_COLUMNS
]

y = df[
    "price"
]


# ============================================================
# ВІДТВОРЕННЯ ТОГО САМОГО ПОДІЛУ
# ============================================================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=RANDOM_STATE
)


X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=RANDOM_STATE
)


# ============================================================
# ЗАВАНТАЖЕННЯ ГОТОВОЇ МОДЕЛІ
# ============================================================

model = joblib.load(
    MODEL_PATH
)


# ============================================================
# ФІНАЛЬНИЙ ПРОГНОЗ НА TEST
# ============================================================

y_test_pred = model.predict(
    X_test
)


# ============================================================
# МЕТРИКИ
# ============================================================

test_mae = mean_absolute_error(
    y_test,
    y_test_pred
)


test_rmse = (
    mean_squared_error(
        y_test,
        y_test_pred
    ) ** 0.5
)


test_r2 = r2_score(
    y_test,
    y_test_pred
)


# ============================================================
# РЕЗУЛЬТАТ
# ============================================================

print("=" * 60)

print(
    "ФІНАЛЬНЕ ОЦІНЮВАННЯ "
    "RANDOM FOREST НА TEST"
)

print("=" * 60)

print(
    f"Кількість тестових записів: "
    f"{len(X_test)}"
)

print()

print(
    f"MAE:  {test_mae:.2f}"
)

print(
    f"RMSE: {test_rmse:.2f}"
)

print(
    f"R2:   {test_r2:.4f}"
)