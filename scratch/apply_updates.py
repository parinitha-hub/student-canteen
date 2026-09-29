import os
import shutil
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -----------------------------------------------------------------------------
# 1. UPDATE backend/app.py
# -----------------------------------------------------------------------------
print("Updating backend/app.py...")
backend_path = os.path.join(ROOT, "backend", "app.py")
with open(backend_path, "r", encoding="utf-8") as f:
    backend_code = f.read()

# Add inventory table to init_db if not already there
if "CREATE TABLE IF NOT EXISTS inventory" not in backend_code:
    table_def = """    # Initialize inventory table for tracking ingredient & prepared stock
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
"""
    backend_code = backend_code.replace("    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS feedback (", table_def + "\n    cursor.execute('''\n        CREATE TABLE IF NOT EXISTS feedback (")

# Update cancel_live_order route to accept cancellation_fee and refund details
old_cancel = '''@app.route("/api/orders/<order_id>/cancel", methods=["POST", "DELETE"])
@app.route("/api/orders/<order_id>", methods=["DELETE"])
def cancel_live_order(order_id):
    """Cancel and remove an order from the active live orders queue."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Delete by id or token
        cursor.execute("DELETE FROM live_orders WHERE id = ? OR token = ?", (order_id, order_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success",
            "message": f"Order {order_id} cancelled and removed from kitchen live queue",
            "cancelled_id": order_id,
            "rows_affected": affected
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500'''

new_cancel = '''@app.route("/api/orders/<order_id>/cancel", methods=["POST", "DELETE"])
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
        return jsonify({"status": "error", "message": str(e)}), 500'''

if old_cancel in backend_code:
    backend_code = backend_code.replace(old_cancel, new_cancel)
elif "cancellation_fee = int" not in backend_code:
    print("Warning: old cancel block not matched exactly in backend/app.py")

# Add inventory endpoints if not present
if '@app.route("/api/inventory"' not in backend_code:
    inv_routes = '''
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
        cursor.execute(\'\'\'
            INSERT OR REPLACE INTO inventory (dish_id, dish_name, category, price, stock, threshold, status, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \'\'\', (dish_id, dish_name, category, price, stock, threshold, status, last_updated))
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
'''
    backend_code = backend_code.replace('@app.route("/api/feedback", methods=["GET"])', inv_routes + '\n@app.route("/api/feedback", methods=["GET"])')

with open(backend_path, "w", encoding="utf-8") as f:
    f.write(backend_code)
print("Updated backend/app.py successfully.")
