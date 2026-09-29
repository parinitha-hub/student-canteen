# AI-Based Canteen Food Demand Prediction

An end-to-end Machine Learning web application designed to forecast daily college canteen food demand, minimize food wastage, prevent stockouts, and optimize meal preparation.

Built in accordance with the project specification guidelines for academic demonstration, college viva review, and real-world canteen operations.

---

## 🌟 Key Highlights

- **Zero-Error Dual-Execution Engine**:
  - **Instant Browser Mode**: Simply double-click `index.html` to run the website immediately in any web browser without needing to start a server or configure Python.
  - **Full-Stack ML Mode**: Connects with a Python Flask REST API leveraging a pre-trained **Random Forest Regressor** ($R^2 \approx 90.9\%$, MAE $12.68$).
- **5 Comprehensive Modules**:
  1. **Dashboard**: High-level KPIs (portioned demand, wastage reduction, model accuracy), 7-day trend charts, item baseline table, and recent forecasts.
  2. **Demand Prediction Tool**: Interactive form with day, weather, holiday status, campus events, previous sales inputs, and 1-click test scenarios ("College Fest Friday", "Rainy Snack Surge", "Exam Week").
  3. **Actionable Recommendations**: Calculates exact expected customer demand *plus* a dynamic safety buffer (+5% to +8%) to avoid stockouts during lunch peaks.
  4. **Analytics & Trends**: Interactive charts for actual vs. predicted trajectory, item demand distribution, and a financial savings calculator.
  5. **College Viva & Guide**: Full academic justifications, feature importances, pipeline diagrams, and viva interview cheat sheet.

- **Simplified 1-Click Portals**:
  - **Student / Customer**: Instant access directly to the Food Menu — no password, no roadblocks, 1-click checkout with pickup token generation.
  - **Kitchen Staff AI**: 1-click access with default PIN (`savitha123`) to unlock AI portion prediction, stockout prevention, and historical demand analytics.
- **Session Persistence**: Automatic memory in `localStorage` — page reloads never kick you out or force you to sign in again.

---

## 🚀 How to Run (Choose Any Method)

### Method 1: Windows 1-Click Launcher (Recommended)
Double-click **`start.bat`**. It automatically checks Python, starts the Flask REST backend in the background, verifies port readiness, and opens the website in your browser at `http://127.0.0.1:5000`.

### Method 2: Instant Browser Mode (Zero Installation)
Simply double-click the **`index.html`** file in this folder. It opens in Google Chrome, Microsoft Edge, or Firefox immediately with the built-in zero-latency client ML engine. No installation or terminal required!

### Method 3: Command Line (Run in Terminal)
```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Run in terminal (use any of these commands):
python run.py
# or:
python app.py
# or:
npm start

# 3. Open in browser:
# http://127.0.0.1:5000
```

### Method 4: Deploy to Vercel (Instant Zero-Backend Cloud Deployment)
This repository is configured for pure static zero-configuration Vercel hosting:
1. Push this repository or upload folder to GitHub.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Select your repository and click **"Deploy"** (Keep all settings default — no framework or build settings needed).
4. Vercel deploys in seconds: root `index.html` is auto-detected directly, with zero serverless function limits and zero build errors!
5. All AI kitchen demand forecasts, order tokens, and kitchen management run with the built-in browser ML engine.

---

## 📂 Project Structure

```text
food order using AI/
├── index.html                     # Root entrypoint for 1-click double-click launch
├── start.bat                      # Windows 1-click launcher
├── requirements.txt               # Python dependencies
├── README.md                      # Documentation & Viva Q&A
│
├── frontend/
│   ├── index.html                 # Main Single Page Web Application
│   ├── css/
│   │   └── style.css              # Modern responsive styling & glassmorphism theme
│   └── js/
│       ├── app.js                 # UI tab navigation, form validation, and state
│       ├── model_engine.js        # High-precision client ML engine (zero-latency fallback)
│       └── charts.js              # SVG / Canvas demand and trend charts
│
├── backend/
│   ├── app.py                     # Flask REST API (/api/predict, /api/history, /api/analytics)
│   └── history.db                 # SQLite database storing prediction history
│
└── ml/
    ├── data/
    │   ├── generate_dataset.py    # Generates realistic multi-month canteen sales data
    │   └── canteen_demand_dataset.csv # 720+ realistic historical observation records
    ├── preprocessing/
    │   └── pipeline.py            # Reproducible ColumnTransformer (OneHotEncoder + Scaler)
    └── models/
        ├── train.py               # Time-aware training script (Baseline vs. Random Forest)
        ├── evaluate.py            # Evaluation metrics & viva report script
        └── saved/
            ├── best_model.pkl     # Trained Random Forest Regressor
            ├── baseline_model.pkl # Trained Linear Regression Model
            ├── preprocessor.pkl   # Fitted Feature Transformer
            └── model_metrics.json # Evaluation scores, residual data, & viva notes
```

---

## 🔬 Machine Learning Methodology

### 1. Dataset Characteristics
- **Dataset Size**: 720 records across 90 continuous operating days.
- **Menu Items**: Veg Biryani, Chicken Biryani, Masala Dosa, Paneer Thali, Chole Bhature, Samosa & Chai, Fried Rice, Sandwich.
- **Key Factors**:
  - `day_of_week` (Monday–Sunday)
  - `weather` (Sunny, Rainy, Cloudy, Cold)
  - `is_holiday` (0 = Regular day, 1 = Holiday/Weekend)
  - `special_event` (None, College Fest, Sports Meet, Exam Period, Workshop)
  - `previous_day_sales` & `previous_week_sales` (Lag features capturing demand momentum)
  - `quantity_sold` (Continuous target variable)

### 2. Time-Aware Validation (Preventing Data Leakage)
To mirror real-world forecasting, data is sorted chronologically:
- **Training Set (80%)**: Dates before 2026-08-20 (576 records).
- **Testing Set (20%)**: Dates from 2026-08-20 onwards (144 unseen records).

### 3. Model Comparison Results

| Metric | Linear Regression (Baseline) | Random Forest Regressor (Selected) | Operational Improvement |
| :--- | :--- | :--- | :--- |
| **Test MAE** | 17.38 portions | **12.68 portions** | **Reduces error by 4.7 meals/item** |
| **Test RMSE** | 22.21 | **16.77** | Penalizes severe forecast spikes |
| **Test $R^2$** | 0.8403 | **0.9090 (~91%)** | Explains 91% of demand variance |

---

## 🎓 College Viva & Review Q&A

1. **Why Random Forest over Linear Regression?**
   - Linear Regression assumes strictly additive relationships. It cannot model complex non-linear compound effects, such as *Rainy Weather* causing a +35% surge in *Samosa & Chai* while simultaneously reducing *Masala Dosa* demand. Random Forest captures non-linear splits effectively without overfitting.

2. **Why not use Deep Learning / Neural Networks?**
   - Deep Learning typically requires tens of thousands of samples and is prone to overfitting on small/medium tabular datasets. Random Forest provides superior performance, stability, and interpretability for this scale.

3. **What is the practical value of MAE (Mean Absolute Error)?**
   - MAE translates directly to meal portions. An MAE of 12.68 means the kitchen forecast is within ~13 portions of actual demand. Combining this with a dynamic safety buffer (+5% to +8%) prevents stockouts during peak hours while cutting surplus waste by ~24.5%.

---

## 🛡️ License & Academic Use
Developed for academic learning, project reviews, and demonstration purposes. Free to modify and adapt.
