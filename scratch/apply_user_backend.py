import os
import sqlite3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backend_path = os.path.join(ROOT, "backend", "app.py")

with open(backend_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update init_db to add users table and user_id/username columns to live_orders
user_table_sql = """    # Initialize users table for user-specific authentication and data isolation
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
"""

if "CREATE TABLE IF NOT EXISTS users" not in code:
    code = code.replace("    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS live_orders (", user_table_sql + "\n    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS live_orders (")
    print("Added users table to init_db in backend/app.py")

# Add columns to live_orders if missing
alter_cols = """    # Add user_id and username columns to live_orders if not present
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN user_id TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE live_orders ADD COLUMN username TEXT")
    except Exception:
        pass
"""
if "ALTER TABLE live_orders ADD COLUMN user_id TEXT" not in code:
    code = code.replace("    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS feedback (", alter_cols + "\n    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS feedback (")
    print("Added ALTER TABLE live_orders columns to backend/app.py")

# 2. Add Authentication API endpoints
auth_endpoints = """
# =========================================================================
# USER-SPECIFIC AUTHENTICATION API
# =========================================================================

@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    \"\"\"Register a new student account with unique credentials and profile.\"\"\"
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
    \"\"\"Authenticate user with username and password, returning their isolated profile.\"\"\"
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
    \"\"\"List registered users (without passwords) for verification.\"\"\"
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
"""

if '@app.route("/api/auth/login"' not in code:
    code = code.replace('@app.route("/api/orders", methods=["GET"])', auth_endpoints + '\n@app.route("/api/orders", methods=["GET"])')
    print("Added auth endpoints to backend/app.py")

# 3. Update get_live_orders to filter by user_id/username if provided
old_get_orders = '''@app.route("/api/orders", methods=["GET"])
def get_live_orders():
    """Retrieve all current live orders for Kitchen Staff and Students."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM live_orders ORDER BY timestamp DESC")
        rows = cursor.fetchall()'''

new_get_orders = '''@app.route("/api/orders", methods=["GET"])
def get_live_orders():
    """Retrieve orders, strictly filtering by user_id/username if specified for student data isolation."""
    try:
        user_id = request.args.get("user_id")
        username = request.args.get("username")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if user_id or username:
            cursor.execute("SELECT * FROM live_orders WHERE user_id = ? OR username = ? ORDER BY timestamp DESC", (user_id or "", username or ""))
        else:
            cursor.execute("SELECT * FROM live_orders ORDER BY timestamp DESC")
        rows = cursor.fetchall()'''

if old_get_orders in code:
    code = code.replace(old_get_orders, new_get_orders)
    print("Updated get_live_orders with user isolation filtering in backend/app.py")

# 4. Update create_live_order to save user_id and username
old_create_order = '''        order_id = data.get("id") or f"ORD-{int(datetime.now().timestamp() * 1000)}"
        token = data.get("token") or "#A-01"
        cust_name = data.get("customer") or data.get("customerName") or data.get("customer_name") or "Student"
        cust_year = data.get("customerYear") or data.get("customer_year") or data.get("year") or "1st Year"
        cust_phone = data.get("customerPhone") or data.get("customer_phone") or data.get("phone") or ""
        items_data = data.get("items") or []
        items_json = json.dumps(items_data) if isinstance(items_data, list) else str(items_data)
        total = int(data.get("total") or 0)
        time_str = data.get("time") or datetime.now().strftime("%I:%M %p")
        status = data.get("status") or "Preparing in Kitchen ⏳"
        timestamp = int(data.get("timestamp") or (datetime.now().timestamp() * 1000))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(\'\'\'
            INSERT OR REPLACE INTO live_orders (
                id, token, customer_name, customer_year, customer_phone,
                items, total, time, status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        \'\'\', (
            order_id, token, cust_name, cust_year, cust_phone,
            items_json, total, time_str, status, timestamp
        ))'''

new_create_order = '''        order_id = data.get("id") or f"ORD-{int(datetime.now().timestamp() * 1000)}"
        token = data.get("token") or "#A-01"
        user_id = data.get("userId") or data.get("user_id") or ""
        username = data.get("username") or ""
        cust_name = data.get("customer") or data.get("customerName") or data.get("customer_name") or "Student"
        cust_year = data.get("customerYear") or data.get("customer_year") or data.get("year") or "1st Year"
        cust_phone = data.get("customerPhone") or data.get("customer_phone") or data.get("phone") or ""
        items_data = data.get("items") or []
        items_json = json.dumps(items_data) if isinstance(items_data, list) else str(items_data)
        total = int(data.get("total") or 0)
        time_str = data.get("time") or datetime.now().strftime("%I:%M %p")
        status = data.get("status") or "Preparing in Kitchen ⏳"
        timestamp = int(data.get("timestamp") or (datetime.now().timestamp() * 1000))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(\'\'\'
            INSERT OR REPLACE INTO live_orders (
                id, token, user_id, username, customer_name, customer_year, customer_phone,
                items, total, time, status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        \'\'\', (
            order_id, token, user_id, username, cust_name, cust_year, cust_phone,
            items_json, total, time_str, status, timestamp
        ))'''

if old_create_order in code:
    code = code.replace(old_create_order, new_create_order)
    print("Updated create_live_order to record user_id and username in backend/app.py")

with open(backend_path, "w", encoding="utf-8") as f:
    f.write(code)

print("backend/app.py updated successfully!")
