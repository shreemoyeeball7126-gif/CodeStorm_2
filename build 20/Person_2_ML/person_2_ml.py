# PERSON 2 — Train the demand forecasting model.
# The project uses the 500-day Person_1_Data/demand_data.csv.
# Run this file to (re)train the model and refresh model_metrics.csv + demand_model.pkl.

from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Person_1_Data" / "demand_data.csv"
MODEL_FILE = Path(__file__).resolve().parent / "demand_model.pkl"
METRICS_FILE = Path(__file__).resolve().parent / "model_metrics.csv"

CATEGORICAL_FEATURES = ["day_of_week", "weather", "event"]
NUMERIC_FEATURES = ["is_weekend", "exam_day", "attendance_pct", "lag_1_consumed", "rolling_7_consumed"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "meals_consumed"


def build_features(df):
    df = df.sort_values("date").reset_index(drop=True)
    df["lag_1_consumed"] = df["meals_consumed"].shift(1)
    df["rolling_7_consumed"] = df["meals_consumed"].shift(1).rolling(7, min_periods=1).mean()
    df = df.dropna(subset=["lag_1_consumed", "rolling_7_consumed"]).reset_index(drop=True)
    return df


def make_pipeline(model):
    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ("num", "passthrough", NUMERIC_FEATURES),
    ])
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def main():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df = build_features(df)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    candidates = {
        "LinearRegression": make_pipeline(LinearRegression()),
        "RandomForest": make_pipeline(RandomForestRegressor(n_estimators=300, random_state=42)),
    }

    results = []
    fitted = {}
    for name, pipe in candidates.items():
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        results.append({"model": name, "MAE": round(mae, 2), "RMSE": round(rmse, 2)})
        fitted[name] = pipe

    metrics_df = pd.DataFrame(results).sort_values("MAE").reset_index(drop=True)
    metrics_df.to_csv(METRICS_FILE, index=False)

    best_name = metrics_df.iloc[0]["model"]
    best_pipeline = fitted[best_name]

    # Refit the chosen model on the full dataset before saving, so the deployed
    # model benefits from every available day.
    best_pipeline.fit(X, y)

    bundle = {
        "model": best_pipeline,
        "features": FEATURES,
        "model_name": best_name,
    }
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(bundle, f)

    print("Metrics:\n", metrics_df)
    print(f"\nSaved best model ({best_name}) to {MODEL_FILE}")


if __name__ == "__main__":
    main()
