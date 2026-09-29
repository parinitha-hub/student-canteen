"""
Training script for AI Canteen Food Demand Prediction.
Implements time-aware train/test split, trains Baseline (Linear Regression)
and Improved (Random Forest Regressor), evaluates both, and saves models & metrics.
"""
import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ml.preprocessing.pipeline import create_preprocessor, prepare_data, save_pipeline, CATEGORICAL_FEATURES, NUMERICAL_FEATURES

DEFAULT_DATASET = os.path.join(ROOT_DIR, "ml", "data", "canteen_demand_dataset.csv")
DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "ml", "models", "saved")

def train_and_evaluate(dataset_path=None, output_dir=None):
    if dataset_path is None:
        dataset_path = DEFAULT_DATASET
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    # Time-aware split: sort by date to prevent future data leakage
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["date", "food_item"]).reset_index(drop=True)

    # 80% Train, 20% Test chronologically
    unique_dates = df["date"].drop_duplicates().sort_values().values
    split_idx = int(len(unique_dates) * 0.8)
    split_date = unique_dates[split_idx]

    train_df = df[df["date"] < split_date].copy()
    test_df = df[df["date"] >= split_date].copy()

    print(f"Total records: {len(df)}")
    print(f"Train records: {len(train_df)} (Dates < {pd.to_datetime(split_date).strftime('%Y-%m-%d')})")
    print(f"Test records:  {len(test_df)} (Dates >= {pd.to_datetime(split_date).strftime('%Y-%m-%d')})")

    X_train_raw, y_train = prepare_data(train_df)
    X_test_raw, y_test = prepare_data(test_df)

    # Fit preprocessor strictly on training data
    preprocessor = create_preprocessor()
    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    feature_names = preprocessor.get_feature_names_out()

    # 1. Baseline Model: Linear Regression
    print("\n--- Training Baseline Model: Linear Regression ---")
    baseline_model = LinearRegression()
    baseline_model.fit(X_train, y_train)

    y_train_base = baseline_model.predict(X_train)
    y_test_base = baseline_model.predict(X_test)

    baseline_metrics = {
        "model_name": "Linear Regression (Baseline)",
        "train_mae": round(float(mean_absolute_error(y_train, y_train_base)), 2),
        "test_mae": round(float(mean_absolute_error(y_test, y_test_base)), 2),
        "train_rmse": round(float(np.sqrt(mean_squared_error(y_train, y_train_base))), 2),
        "test_rmse": round(float(np.sqrt(mean_squared_error(y_test, y_test_base))), 2),
        "train_r2": round(float(r2_score(y_train, y_train_base)), 4),
        "test_r2": round(float(r2_score(y_test, y_test_base)), 4),
    }
    print(f"Baseline Test MAE: {baseline_metrics['test_mae']} | RMSE: {baseline_metrics['test_rmse']} | R^2: {baseline_metrics['test_r2']}")

    # 2. Improved Model: Random Forest Regressor
    print("\n--- Training Improved Model: Random Forest Regressor ---")
    rf_model = RandomForestRegressor(
        n_estimators=120,
        max_depth=14,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    y_train_rf = rf_model.predict(X_train)
    y_test_rf = rf_model.predict(X_test)

    rf_metrics = {
        "model_name": "Random Forest Regressor (Improved)",
        "train_mae": round(float(mean_absolute_error(y_train, y_train_rf)), 2),
        "test_mae": round(float(mean_absolute_error(y_test, y_test_rf)), 2),
        "train_rmse": round(float(np.sqrt(mean_squared_error(y_train, y_train_rf))), 2),
        "test_rmse": round(float(np.sqrt(mean_squared_error(y_test, y_test_rf))), 2),
        "train_r2": round(float(r2_score(y_train, y_train_rf)), 4),
        "test_r2": round(float(r2_score(y_test, y_test_rf)), 4),
    }
    print(f"Random Forest Test MAE: {rf_metrics['test_mae']} | RMSE: {rf_metrics['test_rmse']} | R^2: {rf_metrics['test_r2']}")

    # Calculate Feature Importances
    importances = rf_model.feature_importances_
    clean_feature_names = [f.replace("cat__", "").replace("num__", "") for f in feature_names]
    sorted_idx = np.argsort(importances)[::-1]

    feature_importance_list = [
        {"feature": clean_feature_names[i], "importance": round(float(importances[i]), 4)}
        for i in sorted_idx[:12]
    ]

    # Item baseline demand profiles
    item_stats = {}
    for item, group in df.groupby("food_item"):
        item_stats[item] = {
            "avg_demand": round(float(group["quantity_sold"].mean()), 1),
            "min_demand": int(group["quantity_sold"].min()),
            "max_demand": int(group["quantity_sold"].max()),
            "std_demand": round(float(group["quantity_sold"].std()), 1)
        }

    # Sample comparison records for UI display
    test_sample_df = test_df.tail(20).copy()
    test_sample_pred = rf_model.predict(preprocessor.transform(test_sample_df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES]))
    sample_records = []
    for idx, row in test_sample_df.reset_index().iterrows():
        sample_records.append({
            "date": row["date"].strftime("%Y-%m-%d"),
            "day_of_week": row["day_of_week"],
            "food_item": row["food_item"],
            "weather": row["weather"],
            "special_event": row["special_event"],
            "actual": int(row["quantity_sold"]),
            "predicted": int(round(test_sample_pred[idx])),
            "error": int(round(test_sample_pred[idx])) - int(row["quantity_sold"])
        })

    # Save models and artifacts
    os.makedirs(output_dir, exist_ok=True)
    save_pipeline(preprocessor, os.path.join(output_dir, "preprocessor.pkl"))
    joblib.dump(rf_model, os.path.join(output_dir, "best_model.pkl"))
    joblib.dump(baseline_model, os.path.join(output_dir, "baseline_model.pkl"))

    metrics_payload = {
        "evaluation_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": len(df),
        "train_records": len(train_df),
        "test_records": len(test_df),
        "baseline_model": baseline_metrics,
        "best_model": rf_metrics,
        "feature_importances": feature_importance_list,
        "item_stats": item_stats,
        "sample_evaluation": sample_records,
        "viva_explanation": {
            "why_random_forest": "Random Forest captures complex non-linear interactions between weather conditions, special campus events, and weekly demand cycles without overfitting.",
            "why_time_aware_split": "Standard random train/test split leaks future seasonal demand into past training data. Chronological splitting guarantees realistic real-world forecasting.",
            "why_mae_metric": "Mean Absolute Error directly translates to the average number of meal portions over-prepared or under-prepared."
        }
    }

    metrics_path = os.path.join(output_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"\nModel & metrics saved successfully to {output_dir}/")
    return metrics_payload

if __name__ == "__main__":
    train_and_evaluate()
