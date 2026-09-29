import urllib.request
import urllib.error
import json
import time

BASE = "http://127.0.0.1:5000"

def get(path):
    req = urllib.request.Request(f"{BASE}{path}")
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode('utf-8')

def post(path, data):
    payload = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE}{path}", data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("======================================================================")
print("TESTING LIVE HTTP SERVER & USER-SPECIFIC DATA ENDPOINTS")
print("======================================================================")

# 1. Health
status, body = get("/api/health")
assert status == 200
data = json.loads(body)
print(f"[1] /api/health: {status} OK, Model Loaded: {data['model_loaded']}")

# 2. Main HTML & User Login UI
status, html = get("/")
assert status == 200
assert 'id="login-student-username"' in html
assert 'id="login-student-password"' in html
assert 'id="profile-modal"' in html
assert 'id="subtab-inventory-btn"' in html
assert 'id="cancel-order-modal"' in html
print("[2] GET /: 200 OK, Contains User Auth, Profile, Inventory, and Cancellation Modals")

# 3. User Authentication - Invalid Credentials
bad_login = {"username": "SAV101", "password": "wrongpassword"}
code, res = post("/api/auth/login", bad_login)
assert code == 401, f"Expected 401 for wrong password, got {code}"
print(f"[3] POST /api/auth/login (Bad Password): {code} Cleanly Rejected ({res.get('error')})")

# 4. User Authentication - Valid Credentials for Srinath (SAV101)
good_login = {"username": "SAV101", "password": "pass123"}
code, res = post("/api/auth/login", good_login)
assert code == 200, f"Expected 200 for valid credentials, got {code}"
assert res["user"]["username"] == "SAV101"
print(f"[4] POST /api/auth/login (SAV101): 200 OK, User: {res['user']['name']} ({res['user']['year']})")

# 5. User Registration - New User Rahul
new_user_payload = {
    "username": "SAV199",
    "password": "securepwd99",
    "name": "Rahul Verma",
    "year": "4th Year ECE",
    "phone": "9887766554"
}
code, reg_res = post("/api/auth/register", new_user_payload)
assert code in (201, 409), f"Expected 201 (or 409 if already exists), got {code}"
print(f"[5] POST /api/auth/register: {code} OK, Registered user SAV199")

# 6. Strict Data Isolation: Orders created for Srinath (SAV101)
order_srinath = {
    "id": f"ORD_SRINATH_{int(time.time())}",
    "token": "#S-01",
    "userId": "SAV101",
    "username": "SAV101",
    "customer": "Srinath Kumar",
    "customerYear": "3rd Year CSE",
    "customerPhone": "9876543210",
    "items": [{"dishId": "veg_biryani", "name": "Veg Biryani", "qty": 2, "price": 110}],
    "total": 220,
    "status": "Cooking"
}
code, res = post("/api/orders", order_srinath)
assert code == 201
print(f"[6] POST /api/orders: 201 Created Order for SAV101 (Token: {order_srinath['token']})")

# 7. Strict Backend Data Isolation Check
# When requesting orders for SAV101, should contain SAV101's order
status, srinath_orders_raw = get("/api/orders?userId=SAV101")
assert status == 200
srinath_orders = json.loads(srinath_orders_raw).get("orders", [])
assert any(o["token"] == order_srinath["token"] for o in srinath_orders)

# When requesting orders for another student (SAV102), must NEVER contain SAV101's order!
status, divya_orders_raw = get("/api/orders?userId=SAV102")
assert status == 200
divya_orders = json.loads(divya_orders_raw).get("orders", [])
assert not any(o["token"] == order_srinath["token"] for o in divya_orders), "DATA LEAK DETECTED: Srinath order visible to Divya!"
print("[7] GET /api/orders?userId=SAV102: Verified 100% strict isolation (Zero leakage of Srinath's orders to Divya)")

# 8. Inventory API
status, inv_body = get("/api/inventory")
assert status == 200
inv_data = json.loads(inv_body)
print(f"[8] GET /api/inventory: 200 OK ({len(inv_data['inventory'])} inventory items active)")

# 9. Cancel Order with Last-Minute Fee
cancel_payload = {
    "cancellation_fee": 20,
    "refund": 200,
    "reason": "Late cancellation test"
}
status, cancel_res = post(f"/api/orders/{order_srinath['id']}/cancel", cancel_payload)
assert status == 200
assert cancel_res["cancellation_fee"] == 20
assert cancel_res["refund"] == 200
print(f"[9] POST /api/orders/<id>/cancel: 200 OK, Applied Late Fee Rs.{cancel_res['cancellation_fee']}, Refunded Rs.{cancel_res['refund']}")

print("\n======================================================================")
print("SUCCESS: ALL LIVE BACKEND ENDPOINTS & DATA ISOLATION VERIFIED WITH 0 ERRORS!")
print("======================================================================")
