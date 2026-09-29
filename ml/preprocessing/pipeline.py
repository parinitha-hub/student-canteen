"""
Preprocessing and feature engineering pipeline for AI Canteen Food Demand Prediction.
"""
import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL_FEATURES = ["day_of_week", "weather", "special_event", "food_item"]
NUMERICAL_FEATURES = ["is_holiday", "previous_day_sales", "previous_week_sales"]
TARGET_COLUMN = "quantity_sold"

def create_preprocessor():
    """Creates a ColumnTransformer pipeline for features."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERICAL_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor

def prepare_data(df, is_training=True):
    """
    Extracts features and target from dataframe.
    """
    X = df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy() if TARGET_COLUMN in df.columns else None
    return X, y

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DEFAULT_PREPROCESSOR_PATH = os.path.join(ROOT_DIR, "ml", "models", "saved", "preprocessor.pkl")

def save_pipeline(preprocessor, filepath=None):
    if filepath is None:
        filepath = DEFAULT_PREPROCESSOR_PATH
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(preprocessor, filepath)
    print(f"Saved preprocessor to {filepath}")

def load_pipeline(filepath=None):
    if filepath is None:
        filepath = DEFAULT_PREPROCESSOR_PATH
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Preprocessor file not found at {filepath}")
    return joblib.load(filepath)

