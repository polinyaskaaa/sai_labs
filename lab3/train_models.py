import json
import time
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
import sys

sys.stdout.reconfigure(encoding="utf-8")


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "lab3_shi.csv"
MODELS_DIR = BASE_DIR / "models"

RESULTS_PATH = BASE_DIR / "model_results.csv"
PREDICTIONS_PATH = BASE_DIR / "validation_predictions.csv"
METADATA_PATH = BASE_DIR / "metadata.json"

RANDOM_STATE = 42
TARGET_COLUMN = "price"

CATEGORICAL_COLUMNS = [
    "airline",
    "source_city",
    "departure_time",
    "stops",
    "arrival_time",
    "destination_city",
    "class",
]

NUMERIC_COLUMNS = ["duration", "days_left"]
FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS

MODEL_FILES = {
    "Linear Regression": "linear_regression.joblib",
    "Decision Tree Regressor": "decision_tree.joblib",
    "Random Forest Regressor": "random_forest.joblib",
}


def create_preprocessor():
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
            (
                "numeric",
                StandardScaler(),
                NUMERIC_COLUMNS,
            ),
        ]
    )


def create_models():
    return {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(
            random_state=RANDOM_STATE
        ),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }


def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Не знайдено файл {DATASET_PATH.name}.\n"
            f"Помістіть Clean_Dataset.csv у папку:\n{BASE_DIR}"
        )

    df = pd.read_csv(DATASET_PATH)

    df = df.drop(
        columns=["Unnamed: 0", "flight"],
        errors="ignore",
    )

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "У датасеті відсутні необхідні стовпці: "
            + ", ".join(missing_columns)
        )

    df = df[required_columns].copy()

    if df.isna().any().any():
        missing = df.isna().sum()
        missing = missing[missing > 0]
        raise ValueError(
            "У датасеті знайдено пропущені значення:\n"
            + missing.to_string()
        )

    return df


def main():
    print("=" * 72)
    print("FLIGHT PRICE PREDICTION — НАВЧАННЯ МОДЕЛЕЙ")
    print("=" * 72)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # 70% train, 15% validation, 15% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=RANDOM_STATE,
    )

    print(f"\nУсього записів: {len(df)}")
    print(f"Train:            {len(X_train)}")
    print(f"Validation:       {len(X_val)}")
    print(f"Test:             {len(X_test)}")

    results = []
    validation_table = pd.DataFrame({
        "real_price": y_val.reset_index(drop=True)
    })

    for model_name, estimator in create_models().items():
        print("\n" + "-" * 72)
        print(f"Модель: {model_name}")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", create_preprocessor()),
                ("model", estimator),
            ]
        )

        start_train = time.perf_counter()
        pipeline.fit(X_train, y_train)
        training_time = time.perf_counter() - start_train

        start_predict = time.perf_counter()
        y_pred = pipeline.predict(X_val)
        prediction_time = time.perf_counter() - start_predict

        mae = mean_absolute_error(y_val, y_pred)
        rmse = mean_squared_error(y_val, y_pred) ** 0.5
        r2 = r2_score(y_val, y_pred)

        results.append({
            "Model": model_name,
            "Training Time (s)": training_time,
            "Prediction Time (s)": prediction_time,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })

        validation_table[model_name] = y_pred

        model_path = MODELS_DIR / MODEL_FILES[model_name]
        joblib.dump(pipeline, model_path)

        print(f"Час навчання: {training_time:.3f} с")
        print(f"MAE:           {mae:.3f}")
        print(f"RMSE:          {rmse:.3f}")
        print(f"R^2:            {r2:.5f}")
        print(f"Збережено:     {model_path.name}")

    pd.DataFrame(results).to_csv(
        RESULTS_PATH,
        index=False,
    )

    validation_table.to_csv(
        PREDICTIONS_PATH,
        index=False,
    )

    metadata = {
        "dataset_rows": int(len(df)),
        "train_rows": int(len(X_train)),
        "validation_rows": int(len(X_val)),
        "test_rows": int(len(X_test)),
        "target": TARGET_COLUMN,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "feature_columns": FEATURE_COLUMNS,
        "model_files": MODEL_FILES,
        "categories": {
            column: sorted(
                [
                    str(value)
                    for value in df[column].dropna().unique().tolist()
                ]
            )
            for column in CATEGORICAL_COLUMNS
        },
        "numeric_ranges": {
            column: {
                "min": float(df[column].min()),
                "max": float(df[column].max()),
            }
            for column in NUMERIC_COLUMNS
        },
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\n" + "=" * 72)
    print("НАВЧАННЯ ЗАВЕРШЕНО")
    print("=" * 72)
    print(f"Метрики:  {RESULTS_PATH.name}")
    print(f"Прогнози: {PREDICTIONS_PATH.name}")
    print(f"Метадані: {METADATA_PATH.name}")
    print(f"Моделі:   {MODELS_DIR}")
    print("\nТепер запускайте airline_app.py.")
    print("Повторне навчання при запуску GUI не потрібне.")


if __name__ == "__main__":
    main()
