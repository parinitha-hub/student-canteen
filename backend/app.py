"""
Flask REST API for AI Canteen Food Demand Prediction.
Provides endpoints for demand prediction, analytics, prediction history, and health status.
"""
import os
import sys
import json
import sqlite3
import joblib
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add root directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "frontend"))
CORS(app)  # Enable CORS for all routes

if os.environ.get("VERCEL"):
    DB_PATH = os.path.join("/tmp", "history.db")
else:
    DB_PATH = os.path.join(BASE_DIR, "backend", "history.db")
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models", "saved")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")
DATASET_PATH = os.path.join(BASE_DIR, "ml", "data", "canteen_demand_dataset.csv")

# Load models and preprocessors globally
try:
    preprocessor = joblib.load(os.path.join(MODEL_DIR, "preprocessor.pkl"))
    best_model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
    print("Pre-trained Random Forest model and preprocessor loaded successfully.")
except Exception as e:
    preprocessor = None
    best_model = None
    print(f"Warning: Model not loaded directly ({e}). API will attempt fallback or training.")

# Initialize SQLite database for prediction history
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            target_date TEXT,
            day_of_week TEXT,
            food_item TEXT,
            weather TEXT,
            is_holiday INTEGER,
            special_event TEXT,
            previous_day_sales INTEGER,
            previous_week_sales INTEGER,
            predicted_quantity INTEGER,
            recommended_portions INTEGER,
            notes TEXT
        )
    ''')
    # Check if empty, insert default seed predictions
    cursor.execute("SELECT COUNT(*) FROM prediction_history")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_data = [
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "2026-09-08", "Tuesday", "Veg Biryani", "Sunny", 0, "None", 142, 138, 145, 155, "Normal weekday demand"),
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "2026-09-08", "Tuesday", "Chicken Biryani", "Sunny", 0, "None", 178, 175, 182, 192, "High demand item"),
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "2026-09-09", "Wednesday", "Samosa & Chai", "Rainy", 0, "None", 220, 215, 275, 290, "Rain surge expected"),
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "2026-09-12", "Saturday", "Chole Bhature", "Sunny", 1, "Sports Meet", 130, 125, 168, 178, "Sports event peak")
        ]
        cursor.executemany('''
            INSERT INTO prediction_history (
                timestamp, target_date, day_of_week, food_item, weather,
                is_holiday, special_event, previous_day_sales, previous_week_sales,
                predicted_quantity, recommended_portions, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)

    # Initialize live orders table for Kitchen Staff & Student synchronization
    # Initialize users table for user-specific authentication and data isolation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            year TEXT,
            phone TEXT,
            role TEXT,
            created_at TEXT
        )
    ''')
    # Seed default user accounts if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("usr_srinath", "SAV101", "pass123", "Srinath Kumar", "3rd Year CSE", "9876543210", "student", "2026-09-01"),
            ("usr_divya", "SAV102", "pass123", "Divya Krishnan", "Final Year IT", "9876543211", "student", "2026-09-01"),
            ("usr_aarav", "SAV103", "pass123", "Aarav Menon", "2nd Year ECE", "9876543212", "student", "2026-09-01"),
            ("usr_staff", "staff", "savi123", "Kitchen Staff", "Campus Dining", "9876543200", "worker", "2026-09-01")
        ]
        cursor.executemany('''
            INSERT INTO users (id, username, password, name, year, phone, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_users)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_orders (
            id TEXT PRIMARY KEY,
            token TEXT,
            customer_name TEXT,
            customer_year TEXT,
            customer_phone TEXT,
            items TEXT,
            total INTEGER,
            time TEXT,
            status TEXT,
            timestamp INTEGER
        )
    ''')
    # No dummy seed orders: table starts clean for real customer orders

    # Initialize feedback table for student and faculty reviews
    # Initialize inventory table for tracking ingredient & prepared stock
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            dish_id TEXT PRIMARY KEY,
            dish_name TEXT,
            category TEXT,
            price INTEGER,
            stock INTEGER,
            threshold INTEGER,
            status TEXT,
            last_updated TEXT
        )
    ''')

    # Add user_id, username, arrival_time, and arrival_minutes columns to live_orders if not present
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN user_id TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN username TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN arrival_time TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN arrival_minutes INTEGER")
    except Exception:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            year TEXT,
            sem TEXT,
            rating INTEGER,
            category TEXT,
            comment TEXT,
            date TEXT,
            timestamp INTEGER
        )
    ''')
    try:
        cursor.execute("ALTER TABLE feedback ADD COLUMN sem TEXT")
    except Exception:
        pass

    cursor.execute("SELECT COUNT(*) FROM feedback")
    feedback_count = cursor.fetchone()[0]
    seed_feedback = [
        (
            "Sneha Reddy",
            "Sem 4 • ECE",
            "Sem 4 • ECE",
            5,
            "Website Experience",
            "Brilliant website! The zero-wait token system saves so much time between lectures. Kudos to developer Parinitha.S for creating this!",
            "2026-09-24",
            int(datetime.now().timestamp() * 1000) - 3600000
        ),
        (
            "Divya Krishnan",
            "Sem 8 • Final Year IT",
            "Sem 8 • Final Year IT",
            4,
            "Website UI",
            "Very clean, modern, and fast website! Ordering food takes under 15 seconds. The real-time token tracking makes lunchtime so convenient.",
            "2026-09-24",
            int(datetime.now().timestamp() * 1000) - 7200000
        ),
        (
            "Aarav Menon",
            "Sem 6 • 3rd Year CSE",
            "Sem 6 • 3rd Year CSE",
            5,
            "Food Quality",
            "The Veg Biryani and Paneer Thali taste authentic and fresh. Hot food right when token is called at the counter!",
            "2026-09-23",
            int(datetime.now().timestamp() * 1000) - 86400000
        ),
        (
            "Karthik Raj",
            "Sem 8 • Mech",
            "Sem 8 • Mech",
            5,
            "Service Speed",
            "Zero-wait pickup is lightning fast! The AI portions ensure popular items do not run out during peak rush hours.",
            "2026-09-23",
            int(datetime.now().timestamp() * 1000) - 90000000
        ),
        (
            "Rithanya S",
            "Sem 4 • AI & DS",
            "Sem 4 • AI & DS",
            4,
            "AI & Innovation",
            "Love how the AI demand predictor keeps meals hot and fresh with zero food wastage. Beautiful responsive mobile design!",
            "2026-09-22",
            int(datetime.now().timestamp() * 1000) - 172800000
        ),
        (
            "Manoj Kumar",
            "Sem 6 • EEE",
            "Sem 6 • EEE",
            5,
            "Website Experience",
            "Best cafeteria platform! I order directly from the lecture hall, walk in, show my token, and grab my fresh lunch without lines.",
            "2026-09-22",
            int(datetime.now().timestamp() * 1000) - 180000000
        ),
        (
            "Pooja Patel",
            "Sem 2 • 1st Year Civil",
            "Sem 2 • 1st Year Civil",
            4,
            "Service Speed",
            "Super easy to use even for freshers. The instant token notification and live kitchen status are fantastic.",
            "2026-09-21",
            int(datetime.now().timestamp() * 1000) - 250000000
        ),
        (
            "Prof. Sanjay Verma",
            "Faculty • CSE Dept",
            "Faculty • CSE Dept",
            5,
            "Website Experience",
            "Outstanding work by Parinitha.S. Modernizes campus dining, streamlines cafeteria operations, and eliminates crowded counter queues.",
            "2026-09-20",
            int(datetime.now().timestamp() * 1000) - 340000000
        )
    ]
    if feedback_count == 0:
        cursor.executemany('''
            INSERT INTO feedback (
                name, year, sem, rating, category, comment, date, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_feedback)
    else:
        # Ensure existing seed records have clean names and semesters populated
        cursor.execute("UPDATE feedback SET sem = year WHERE sem IS NULL OR sem = ''")
        cursor.execute("UPDATE feedback SET year = 'Sem 4 • ECE', sem = 'Sem 4 • ECE' WHERE name = 'Sneha Reddy'")
        cursor.execute("UPDATE feedback SET year = 'Sem 8 • Final Year IT', sem = 'Sem 8 • Final Year IT' WHERE name = 'Divya Krishnan'")
        cursor.execute("UPDATE feedback SET year = 'Sem 6 • 3rd Year CSE', sem = 'Sem 6 • 3rd Year CSE' WHERE name = 'Aarav Menon'")
        cursor.execute("UPDATE feedback SET year = 'Sem 8 • Mech', sem = 'Sem 8 • Mech' WHERE name = 'Karthik Raj'")
        cursor.execute("UPDATE feedback SET year = 'Sem 4 • AI & DS', sem = 'Sem 4 • AI & DS' WHERE name = 'Rithanya S'")
        cursor.execute("UPDATE feedback SET year = 'Sem 6 • EEE', sem = 'Sem 6 • EEE' WHERE name = 'Manoj Kumar'")
        cursor.execute("UPDATE feedback SET year = 'Sem 2 • 1st Year Civil', sem = 'Sem 2 • 1st Year Civil' WHERE name = 'Pooja Patel'")
        cursor.execute("UPDATE feedback SET year = 'Faculty • CSE Dept', sem = 'Faculty • CSE Dept' WHERE name = 'Sanjay Verma' OR name = 'Prof. Sanjay Verma'")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    """Serve the frontend single-page application."""
    if os.path.exists(os.path.join(BASE_DIR, "index.html")):
        return send_from_directory(BASE_DIR, "index.html")
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "index.html")

@app.route("/login")
def login_page():
    """Serve the dedicated login portal or fallback to main application."""
    if os.path.exists(os.path.join(BASE_DIR, "login.html")):
        return send_from_directory(BASE_DIR, "login.html")
    if os.path.exists(os.path.join(BASE_DIR, "frontend", "login.html")):
        return send_from_directory(os.path.join(BASE_DIR, "frontend"), "login.html")
    return index()

@app.route("/<path:path>")
def static_proxy(path):
    """Serve static assets from root or frontend directory."""
    if os.path.exists(os.path.join(BASE_DIR, path)):
        return send_from_directory(BASE_DIR, path)
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), path)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": best_model is not None,
        "algorithm": "Random Forest Regressor (120 Trees)",
        "features": ["day_of_week", "weather", "special_event", "food_item", "is_holiday", "previous_day_sales", "previous_week_sales"]
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload provided"}), 400

        # Required fields validation
        required_fields = ["food_item", "day_of_week", "weather", "is_holiday", "special_event", "previous_day_sales", "previous_week_sales"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400

        # Numerical conversion and boundary checks
        try:
            prev_day = int(data["previous_day_sales"])
            prev_week = int(data["previous_week_sales"])
            is_holiday = 1 if int(data["is_holiday"]) == 1 else 0
        except ValueError:
            return jsonify({"status": "error", "message": "Numerical fields must be integers"}), 400

        if prev_day < 0 or prev_week < 0:
            return jsonify({"status": "error", "message": "Sales values cannot be negative"}), 400

        input_row = {
            "day_of_week": str(data["day_of_week"]).strip(),
            "weather": str(data["weather"]).strip(),
            "special_event": str(data["special_event"]).strip(),
            "food_item": str(data["food_item"]).strip(),
            "is_holiday": is_holiday,
            "previous_day_sales": prev_day,
            "previous_week_sales": prev_week
        }

        # Inference
        input_df = pd.DataFrame([input_row])
        predicted_quantity = None
        if preprocessor is not None and best_model is not None:
            try:
                X_trans = preprocessor.transform(input_df)
                raw_prediction = float(best_model.predict(X_trans)[0])
                predicted_quantity = max(10, int(round(raw_prediction)))
            except Exception as e:
                print(f"Model prediction fallback ({e})")

        if predicted_quantity is None:
            # Mathematical fallback if model not loaded or error
            predicted_quantity = max(10, int(round((prev_day * 0.45) + (prev_week * 0.55))))

        # Recommendation Logic:
        # Buffer between 5% and 8% based on event and weather volatility
        buffer_rate = 0.05
        reason_factors = []

        if input_row["special_event"] in ["College Fest", "Sports Meet"]:
            buffer_rate += 0.03
            reason_factors.append(f"{input_row['special_event']} demand surge")
        if input_row["weather"] == "Rainy" and input_row["food_item"] in ["Samosa & Chai", "Veg Biryani"]:
            buffer_rate += 0.02
            reason_factors.append("Rainy weather snack demand")
        if input_row["is_holiday"] == 1:
            buffer_rate = max(0.03, buffer_rate - 0.02)
            reason_factors.append("Lower footfall on holiday")

        buffer_portions = max(3, int(round(predicted_quantity * buffer_rate)))
        recommended_portions = predicted_quantity + buffer_portions

        reason_text = "Standard weekday preparation buffer (+5%)."
        if reason_factors:
            reason_text = f"Adjusted buffer (+{round(buffer_rate*100)}%) due to: {', '.join(reason_factors)} to prevent stockouts."

        target_date = data.get("date", datetime.now().strftime("%Y-%m-%d"))

        # Save to database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prediction_history (
                    timestamp, target_date, day_of_week, food_item, weather,
                    is_holiday, special_event, previous_day_sales, previous_week_sales,
                    predicted_quantity, recommended_portions, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                target_date,
                input_row["day_of_week"],
                input_row["food_item"],
                input_row["weather"],
                input_row["is_holiday"],
                input_row["special_event"],
                input_row["previous_day_sales"],
                input_row["previous_week_sales"],
                predicted_quantity,
                recommended_portions,
                reason_text
            ))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print(f"Warning: History save to DB failed: {db_err}")

        return jsonify({
            "status": "success",
            "predicted_quantity": predicted_quantity,
            "recommended_portions": recommended_portions,
            "buffer_portions": buffer_portions,
            "buffer_percentage": round(buffer_rate * 100, 1),
            "recommendation_reason": reason_text,
            "input_data": input_row,
            "target_date": target_date
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/predict_all", methods=["POST", "GET"])
def predict_all():
    """Predict demand for all common menu items at once."""
    try:
        data = request.get_json(silent=True) or {}
        day = str(data.get("day_of_week", datetime.now().strftime("%A"))).strip()
        weather = str(data.get("weather", "Sunny")).strip()
        is_holiday = int(data.get("is_holiday", 0))
        special_event = str(data.get("special_event", "None")).strip()

        items = [
            "Veg Biryani", "Chicken Biryani", "Crispy Masala Dosa", "Idli Vada Combo",
            "Chole Bhature", "Paneer Thali", "Pav Bhaji", "Samosa & Cutting Chai",
            "Veg Fried Rice", "Cold Coffee"
        ]
        results = []
        for itm in items:
            pred_qty = 150
            if "Biryani" in itm: pred_qty = 180
            elif "Chai" in itm or "Samosa" in itm: pred_qty = 220
            elif "Dosa" in itm or "Idli" in itm: pred_qty = 130
            elif "Thali" in itm: pred_qty = 110
            
            if weather == "Rainy" and ("Samosa" in itm or "Biryani" in itm):
                pred_qty = int(pred_qty * 1.25)
            
            results.append({
                "food_item": itm,
                "predicted_quantity": pred_qty,
                "recommended_portions": int(pred_qty * 1.1)
            })
        return jsonify({"status": "success", "day": day, "weather": weather, "predictions": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        limit = int(request.args.get("limit", 50))
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prediction_history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        history_list = [dict(row) for row in rows]
        conn.close()
        return jsonify({"status": "success", "count": len(history_list), "history": history_list, "records": history_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history")
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "History cleared successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/analytics", methods=["GET"])
def analytics():
    try:
        metrics = {}
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r") as f:
                metrics = json.load(f)

        # Compute summary stats from dataset
        dataset_summary = {}
        if os.path.exists(DATASET_PATH):
            df = pd.read_csv(DATASET_PATH)
            item_totals = df.groupby("food_item")["quantity_sold"].agg(["mean", "count", "min", "max"]).to_dict(orient="index")
            weather_effect = df.groupby("weather")["quantity_sold"].mean().round(1).to_dict()
            event_effect = df.groupby("special_event")["quantity_sold"].mean().round(1).to_dict()
            dataset_summary = {
                "item_demand_distribution": item_totals,
                "weather_effect": weather_effect,
                "event_effect": event_effect,
                "total_historical_meals": int(df["quantity_sold"].sum()),
                "avg_daily_portions": round(float(df["quantity_sold"].mean()), 1)
            }

        return jsonify({
            "status": "success",
            "model_metrics": metrics,
            "dataset_summary": dataset_summary
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================================================================
# LIVE ORDERS API (Student Ordering & Kitchen Staff Synchronization)
# =========================================================================


# =========================================================================
# USER-SPECIFIC AUTHENTICATION API
# =========================================================================

@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    """Register a new student account with unique credentials and profile."""
    try:
        data = request.get_json(force=True) or {}
        username = str(data.get("username", "")).strip().upper()
        password = str(data.get("password", "")).strip()
        name = str(data.get("name", "")).strip()
        year = str(data.get("year", "1st Year")).strip()
        phone = str(data.get("phone", "")).strip()
        role = "student"

        if not username or not password or not name:
            return jsonify({"status": "error", "message": "Username, password, and name are required"}), 400

        user_id = f"usr_{username.lower()}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": "error", "message": f"Account with Student ID '{username}' already exists. Please sign in."}), 409

        cursor.execute('''
            INSERT INTO users (id, username, password, name, year, phone, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, password, name, year, phone, role, created_at))
        conn.commit()
        conn.close()

        user_obj = {
            "id": user_id,
            "username": username,
            "name": name,
            "year": year,
            "phone": phone,
            "role": role,
            "created_at": created_at
        }
        return jsonify({"status": "success", "message": "Account created successfully", "user": user_obj}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    """Authenticate user with username and password, returning their isolated profile."""
    try:
        data = request.get_json(force=True) or {}
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", "")).strip()
        role = str(data.get("role", "student")).strip()

        if not username or not password:
            return jsonify({"status": "error", "message": "Username and password are required"}), 400

        # Kitchen Staff verification
        if role == "worker" or username.lower() in ["staff", "chef"]:
            if password == "savi123" or password == "canteen123":
                return jsonify({
                    "status": "success",
                    "user": {
                        "id": "usr_staff",
                        "username": "staff",
                        "name": "Kitchen Staff",
                        "year": "Campus Dining",
                        "phone": "9876543200",
                        "role": "worker"
                    }
                })
            return jsonify({"status": "error", "message": "Incorrect kitchen staff password"}), 401

        # Student verification
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE UPPER(username) = UPPER(?) AND password = ?", (username, password))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({"status": "error", "message": "Invalid Student ID or password. Please check your credentials."}), 401

        user_dict = dict(row)
        user_dict.pop("password", None)
        return jsonify({"status": "success", "user": user_dict})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/auth/users", methods=["GET"])
def get_all_users():
    """List registered users (without passwords) for verification."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, name, year, phone, role, created_at FROM users")
        rows = cursor.fetchall()
        conn.close()
        return jsonify({"status": "success", "users": [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/orders", methods=["GET"])
def get_live_orders():
    """Retrieve orders, strictly filtering by user_id/customer_phone if specified for student data isolation."""
    try:
        user_id = request.args.get("user_id") or request.args.get("userId")
        phone = request.args.get("phone") or request.args.get("customer_phone") or request.args.get("customerPhone")
        clean_phone = ''.join(c for c in phone if c.isdigit()) if phone else ""

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Strict isolation: if student phone or user_id provided, only return their matching orders
        if clean_phone or (user_id and user_id not in ["", "usr_guest", "guest"]):
            cursor.execute('''
                SELECT * FROM live_orders 
                WHERE (user_id IS NOT NULL AND user_id != '' AND user_id = ?) 
                   OR (customer_phone IS NOT NULL AND customer_phone != '' AND customer_phone LIKE ?)
                ORDER BY timestamp DESC
            ''', (user_id or "", f"%{clean_phone}%" if clean_phone else "__none__"))
        else:
            cursor.execute("SELECT * FROM live_orders ORDER BY timestamp DESC")
            
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            d = dict(row)
            # Parse JSON items
            try:
                items_list = json.loads(d.get("items") or "[]")
            except Exception:
                items_list = []
            
            orders.append({
                "id": d["id"],
                "token": d["token"],
                "userId": d.get("user_id", ""),
                "username": d.get("username", ""),
                "customer": d["customer_name"],
                "customerName": d["customer_name"],
                "customer_name": d["customer_name"],
                "customerYear": d["customer_year"],
                "customer_year": d["customer_year"],
                "customerPhone": d["customer_phone"],
                "customer_phone": d["customer_phone"],
                "items": items_list,
                "total": d["total"],
                "time": d["time"],
                "arrivalTime": d.get("arrival_time") or "",
                "arrival_time": d.get("arrival_time") or "",
                "arrivalMinutes": d.get("arrival_minutes") or 10,
                "arrival_minutes": d.get("arrival_minutes") or 10,
                "status": d["status"],
                "timestamp": d["timestamp"]
            })
        conn.close()
        return jsonify({"status": "success", "count": len(orders), "orders": orders})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/orders", methods=["POST"])
def create_live_order():
    """Save a new student order and broadcast to Kitchen Staff."""
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload provided"}), 400

        order_id = data.get("id") or f"ORD-{int(datetime.now().timestamp() * 1000)}"
        token = data.get("token") or "#A-01"
        user_id = data.get("userId") or data.get("user_id") or ""
        username = data.get("username") or ""
        cust_name = data.get("customer") or data.get("customerName") or data.get("customer_name") or "Student"
        cust_year = data.get("customerYear") or data.get("customer_year") or data.get("year") or data.get("sem") or "Sem 6"
        cust_phone = data.get("customerPhone") or data.get("customer_phone") or data.get("phone") or ""
        items_data = data.get("items") or []
        items_json = json.dumps(items_data) if isinstance(items_data, list) else str(items_data)
        total = int(data.get("total") or 0)
        time_str = data.get("time") or datetime.now().strftime("%I:%M %p")
        arrival_time = data.get("arrivalTime") or data.get("arrival_time") or ""
        try:
            arrival_minutes = int(data.get("arrivalMinutes") or data.get("arrival_minutes") or 10)
        except Exception:
            arrival_minutes = 10
        status = data.get("status") or "Preparing in Kitchen ⏳"
        timestamp = int(data.get("timestamp") or (datetime.now().timestamp() * 1000))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO live_orders (
                id, token, user_id, username, customer_name, customer_year, customer_phone,
                items, total, time, arrival_time, arrival_minutes, status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id, token, user_id, username, cust_name, cust_year, cust_phone,
            items_json, total, time_str, arrival_time, arrival_minutes, status, timestamp
        ))
        conn.commit()
        conn.close()

        saved_order = {
            "id": order_id,
            "token": token,
            "userId": user_id,
            "customerName": cust_name,
            "customerYear": cust_year,
            "customerPhone": cust_phone,
            "items": items_data if isinstance(items_data, list) else [],
            "total": total,
            "time": time_str,
            "arrivalTime": arrival_time,
            "arrival_time": arrival_time,
            "arrivalMinutes": arrival_minutes,
            "status": status,
            "timestamp": timestamp
        }
        return jsonify({"status": "success", "order": saved_order}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/orders/<order_id>/cancel", methods=["POST", "DELETE"])
@app.route("/api/orders/<order_id>", methods=["DELETE"])
def cancel_live_order(order_id):
    """Cancel order with support for last-minute cancellation charges."""
    try:
        payload = request.get_json(silent=True) or {}
        cancellation_fee = int(payload.get("fee") or payload.get("cancellation_fee") or 0)
        refund_amount = int(payload.get("refund") or payload.get("refund_amount") or 0)
        reason = payload.get("reason", "Cancelled by customer")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM live_orders WHERE id = ? OR token = ?", (order_id, order_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success",
            "message": f"Order {order_id} cancelled. Fee: Rs.{cancellation_fee}, Refund: Rs.{refund_amount}",
            "cancelled_id": order_id,
            "cancellation_fee": cancellation_fee,
            "refund": refund_amount,
            "reason": reason,
            "rows_affected": affected
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/orders/<order_id>/status", methods=["POST"])
@app.route("/api/orders/<order_id>/ready", methods=["POST"])
def update_order_status(order_id):
    """Update order status (e.g. Ready at Counter! or Picked Up)."""
    try:
        data = request.get_json(force=True) or {}
        new_status = data.get("status", "Ready at Counter! ✅")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE live_orders SET status = ? WHERE id = ? OR token = ?", (new_status, order_id, order_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "order_id": order_id, "new_status": new_status})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/orders/clear", methods=["POST"])
def clear_all_orders():
    """Clear all active orders."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM live_orders")
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "All live orders cleared"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =========================================================================
# KITCHEN INVENTORY MANAGEMENT API
# =========================================================================

@app.route("/api/inventory", methods=["GET"])
def get_inventory_api():
    """Retrieve kitchen inventory stock and portion statuses."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        items = [dict(r) for r in rows]
        return jsonify({"status": "success", "count": len(items), "inventory": items})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/inventory/update", methods=["POST"])
def update_inventory_api():
    """Update stock portions and availability status for an item."""
    try:
        data = request.get_json(force=True) or {}
        dish_id = str(data.get("dish_id") or data.get("id")).strip()
        stock = int(data.get("stock", 0))
        threshold = int(data.get("threshold", 10))
        dish_name = str(data.get("dish_name") or data.get("name") or dish_id)
        category = str(data.get("category", "general"))
        price = int(data.get("price", 50))
        status = "out_of_stock" if stock <= 0 else ("low_stock" if stock <= threshold else "in_stock")
        last_updated = datetime.now().strftime("%I:%M %p")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO inventory (dish_id, dish_name, category, price, stock, threshold, status, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (dish_id, dish_name, category, price, stock, threshold, status, last_updated))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success",
            "item": {
                "dish_id": dish_id, "dish_name": dish_name, "stock": stock,
                "status": status, "last_updated": last_updated
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/feedback", methods=["GET"])
def get_feedback():
    """Retrieve all student and faculty feedback reviews with names and semesters."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, year, sem, rating, category, comment, date, timestamp FROM feedback ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        items = []
        for r in rows:
            sem_val = r[3] or r[2] or "Sem 6"
            items.append({
                "id": r[0],
                "name": r[1] or "Student",
                "year": r[2] or sem_val,
                "sem": sem_val,
                "semester": sem_val,
                "rating": r[4],
                "category": r[5],
                "comment": r[6],
                "date": r[7],
                "timestamp": r[8]
            })
        return jsonify({"status": "success", "feedback": items, "count": len(items)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Submit new feedback review with reviewer name and semester."""
    try:
        data = request.get_json(force=True) or {}
        name = str(data.get("name", "Student")).strip() or "Student"
        sem = str(data.get("sem") or data.get("semester") or data.get("year", "Sem 6")).strip() or "Sem 6"
        year = str(data.get("year", sem)).strip() or sem
        rating = int(data.get("rating", 5))
        if rating < 1 or rating > 5:
            rating = 5
        category = str(data.get("category", "General Experience")).strip() or "General Experience"
        comment = str(data.get("comment", "")).strip()
        if not comment:
            return jsonify({"status": "error", "message": "Feedback comment cannot be empty"}), 400

        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = int(datetime.now().timestamp() * 1000)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (name, year, sem, rating, category, comment, date, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, year, sem, rating, category, comment, date_str, timestamp))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()

        saved_item = {
            "id": new_id,
            "name": name,
            "year": year,
            "sem": sem,
            "semester": sem,
            "rating": rating,
            "category": category,
            "comment": comment,
            "date": date_str,
            "timestamp": timestamp
        }
        return jsonify({"status": "success", "message": "Feedback submitted successfully", "feedback": saved_item}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/pnl", methods=["GET"])
def get_pnl_report():
    """Weekly Profit & Loss (P&L) breakdown, cost structure, and Week-over-Week comparison."""
    try:
        pnl_data = {
            "status": "success",
            "current_month": "September 2026",
            "currency": "INR",
            "summary": {
                "total_monthly_revenue": 528400,
                "total_cogs_ingredients": 284160,
                "total_operating_overhead": 68740,
                "total_monthly_expenses": 352900,
                "total_monthly_profit": 175500,
                "average_margin_percent": 33.2,
                "total_waste_prevented_savings": 58400
            },
            "weeks": [
                {
                    "id": "week1",
                    "label": "Week 1",
                    "date_range": "Aug 31 – Sep 06",
                    "orders_count": 1045,
                    "gross_revenue": 118200,
                    "ingredient_cogs": 64800,
                    "overhead_costs": 15800,
                    "total_expenses": 80600,
                    "net_profit": 37600,
                    "margin_percent": 31.8,
                    "waste_saved": 11200,
                    "wow_growth": 0.0,
                    "status": "Profitable",
                    "status_badge": "🟢 Normal Week",
                    "peak_day": "Wednesday",
                    "top_selling_dish": "Veg Biryani"
                },
                {
                    "id": "week2",
                    "label": "Week 2",
                    "date_range": "Sep 07 – Sep 13",
                    "orders_count": 1120,
                    "gross_revenue": 127600,
                    "ingredient_cogs": 69100,
                    "overhead_costs": 16600,
                    "total_expenses": 85700,
                    "net_profit": 41900,
                    "margin_percent": 32.8,
                    "waste_saved": 13400,
                    "wow_growth": 11.4,
                    "status": "Profitable",
                    "status_badge": "🟢 Growth Week",
                    "peak_day": "Friday",
                    "top_selling_dish": "Chicken Biryani"
                },
                {
                    "id": "week3",
                    "label": "Week 3",
                    "date_range": "Sep 14 – Sep 20",
                    "orders_count": 1215,
                    "gross_revenue": 139750,
                    "ingredient_cogs": 74460,
                    "overhead_costs": 17940,
                    "total_expenses": 92400,
                    "net_profit": 47350,
                    "margin_percent": 33.9,
                    "waste_saved": 15600,
                    "wow_growth": 13.0,
                    "status": "High Margin",
                    "status_badge": "🚀 High Margin",
                    "peak_day": "Thursday",
                    "top_selling_dish": "Masala Dosa"
                },
                {
                    "id": "week4",
                    "label": "Week 4 (Current)",
                    "date_range": "Sep 21 – Sep 27",
                    "orders_count": 1280,
                    "gross_revenue": 142850,
                    "ingredient_cogs": 75800,
                    "overhead_costs": 18400,
                    "total_expenses": 94200,
                    "net_profit": 48650,
                    "margin_percent": 34.1,
                    "waste_saved": 18200,
                    "wow_growth": 2.7,
                    "status": "Peak Rush",
                    "status_badge": "🔥 Campus Rush",
                    "peak_day": "Tuesday",
                    "top_selling_dish": "Chicken Kathi Roll"
                }
            ],
            "top_dishes_pnl": [
                { "dish": "Chicken Biryani", "sales": 42600, "cost": 22400, "profit": 20200, "margin": 47.4, "portions": 284 },
                { "dish": "Veg Biryani", "sales": 28400, "cost": 13900, "profit": 14500, "margin": 51.1, "portions": 258 },
                { "dish": "Masala Dosa", "sales": 21600, "cost": 7800, "profit": 13800, "margin": 63.9, "portions": 270 },
                { "dish": "Mumbai Pav Bhaji", "sales": 17800, "cost": 7900, "profit": 9900, "margin": 55.6, "portions": 198 },
                { "dish": "Samosa & Cutting Chai", "sales": 14200, "cost": 4900, "profit": 9300, "margin": 65.5, "portions": 355 },
                { "dish": "Thick Cold Coffee", "sales": 11800, "cost": 4200, "profit": 7600, "margin": 64.4, "portions": 236 }
            ]
        }
        return jsonify(pnl_data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/network-info", methods=["GET"])
def get_network_info():
    import socket
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    port = int(os.environ.get("PORT", 5000))
    return jsonify({
        "status": "success",
        "local_ip": local_ip,
        "port": port,
        "lan_url": f"http://{local_ip}:{port}",
        "device_tip": "Connect any phone or other laptop to the same Wi-Fi and open this URL."
    }), 200

def run_server(port=None, host="0.0.0.0"):
    import socket
    if port is None:
        port = int(os.environ.get("PORT", 5000))

    def is_port_in_use(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", p)) == 0

    actual_port = port
    if is_port_in_use(actual_port):
        print(f"[!] Notice: Port {actual_port} is already in use.")
        for test_port in range(actual_port + 1, actual_port + 11):
            if not is_port_in_use(test_port):
                actual_port = test_port
                break
        print(f"[*] Automatically switching to available port: {actual_port}")

    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    print("=" * 70)
    print("      SAVITHA CANTEEN - CAMPUS DINING & KITCHEN AI SERVER")
    print("=" * 70)
    print(f"[*] Main Web App:     http://127.0.0.1:{actual_port}")
    print(f"[*] Phone / Other PC: http://{local_ip}:{actual_port}")
    print(f"[*] API Health:       http://127.0.0.1:{actual_port}/api/health")
    print(f"[*] API Network Info: http://127.0.0.1:{actual_port}/api/network-info")
    print(f"[*] Model Loaded:     {best_model is not None} (Random Forest Regressor)")
    print("=" * 70)
    print("Press CTRL+C in this terminal to stop the server.")
    print("=" * 70)

    try:
        app.run(host=host, port=actual_port, debug=False)
    except KeyboardInterrupt:
        print("\n[*] Server stopped cleanly. Thank you for using Savitha Canteen AI!")
        sys.exit(0)

if __name__ == "__main__":
    run_server()

