"""
Independent evaluation and reporting script for AI Canteen Food Demand Prediction.
"""
import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DEFAULT_MODELS_DIR = os.path.join(ROOT_DIR, "ml", "models", "saved")
DEFAULT_DATASET = os.path.join(ROOT_DIR, "ml", "data", "canteen_demand_dataset.csv")

def evaluate_saved_model(models_dir=None, dataset_path=None):
    if models_dir is None:
        models_dir = DEFAULT_MODELS_DIR
    if dataset_path is None:
        dataset_path = DEFAULT_DATASET

    metrics_file = os.path.join(models_dir, "model_metrics.json")
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
        
        print("="*60)
        print(" AI CANTEEN DEMAND PREDICTION - MODEL EVALUATION REPORT ")
        print("="*60)
        print(f"Total Dataset Records: {metrics['total_records']}")
        print(f"Train / Test Split:    {metrics['train_records']} train / {metrics['test_records']} test")
        print("\n[MODEL COMPARISON]")
        print(f"1. {metrics['baseline_model']['model_name']}:")
        print(f"   - Test MAE:  {metrics['baseline_model']['test_mae']} portions")
        print(f"   - Test RMSE: {metrics['baseline_model']['test_rmse']}")
        print(f"   - Test R^2:  {metrics['baseline_model']['test_r2']}")
        print(f"\n2. {metrics['best_model']['model_name']}:")
        print(f"   - Test MAE:  {metrics['best_model']['test_mae']} portions (Reduced error by {round(metrics['baseline_model']['test_mae'] - metrics['best_model']['test_mae'], 2)} meals)")
        print(f"   - Test RMSE: {metrics['best_model']['test_rmse']}")
        print(f"   - Test R^2:  {metrics['best_model']['test_r2']} (~{round(metrics['best_model']['test_r2']*100, 1)}% variance explained)")
        
        print("\n[TOP PREDICTIVE FEATURES]")
        for item in metrics["feature_importances"][:6]:
            print(f"   - {item['feature']}: {round(item['importance']*100, 2)}%")
        
        print("\n[VIVA PREPARATION EXPLANATIONS]")
        for k, v in metrics["viva_explanation"].items():
            print(f"   * {k}: {v}")
        print("="*60)
        return metrics
    else:
        print(f"Metrics file not found at {metrics_file}. Run train.py first.")
        return None

if __name__ == "__main__":
    evaluate_saved_model()

