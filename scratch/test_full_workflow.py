import urllib.request
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://127.0.0.1:5000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        return res.status, json.loads(res.read().decode('utf-8'))

def post(path, data):
    url = f"{BASE_URL}{path}"
    payload = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        return res.status, json.loads(res.read().decode('utf-8'))

print("=== 1. TEST SERVER HEALTH ===")
status, health = get("/api/health")
print("Health Status:", status, health.get("status"))
assert status == 200

print("\n=== 2. TEST REVIEWS WITH NAME AND SEM ===")
status, fb_data = get("/api/feedback")
assert status == 200
reviews = fb_data.get("feedback", [])
print(f"Total reviews in database: {len(reviews)}")
for r in reviews[:4]:
    print(f"  • Name: {r.get('name')} | Sem: {r.get('sem')} | Rating: {r.get('rating')}★")
    assert r.get('name'), "Review must have a name"
    assert r.get('sem'), "Review must have a sem"

print("\n=== 3. TEST POSTING NEW REVIEW WITH NAME AND SEM ===")
new_review = {
    "name": "Ananya Sharma",
    "sem": "Sem 5 • Computer Science",
    "year": "Sem 5 • Computer Science",
    "rating": 5,
    "category": "Food & Service",
    "comment": "Super convenient! No lines, and my biryani was ready right when I walked up."
}
status, post_res = post("/api/feedback", new_review)
print("Post Review Status:", status)
assert status in (200, 201)
print("Returned Review:", post_res.get("feedback", {}).get("name"), "|", post_res.get("feedback", {}).get("sem"))

print("\n=== 4. TEST USER A ORDER WITH ARRIVAL TIME ===")
import time
ts = str(int(time.time()))[-6:]
user_a_phone = f"98{ts}10"
user_b_phone = f"91{ts}20"
user_a_order = {
    "id": "ord_test_user_a",
    "token": "#A-88",
    "userId": "usr_" + user_a_phone,
    "user_id": "usr_" + user_a_phone,
    "customer": "Rahul Sharma",
    "customerName": "Rahul Sharma",
    "customer_name": "Rahul Sharma",
    "customerPhone": user_a_phone,
    "customer_phone": user_a_phone,
    "customerYear": "Sem 4 • 2nd Year",
    "items": [{"dishId": "veg_biryani", "name": "Veg Biryani", "qty": 2, "price": 110}],
    "total": 220,
    "time": "12:30 PM",
    "arrivalTime": "12:42 PM",
    "arrival_time": "12:42 PM",
    "arrivalMinutes": 12,
    "arrival_minutes": 12,
    "status": "Cooking"
}
status, order_res = post("/api/orders", user_a_order)
print("User A Order Status:", status)
assert status in (200, 201)

print("\n=== 5. TEST USER B ORDER ISOLATION (SHOULD SEE 0 OF USER A's ORDERS) ===")
status, user_b_orders = get(f"/api/orders?phone={user_b_phone}")
print(f"User B (Phone {user_b_phone}) fetched orders count: {len(user_b_orders.get('orders', []))}")
# User B has not placed an order yet, so User B's orders MUST be 0!
assert len(user_b_orders.get("orders", [])) == 0, "User B should NOT see User A's orders!"
print("✓ SUCCESS: User B sees 0 orders. User A's order is completely isolated!")

print("\n=== 6. TEST USER B PLACING AN ORDER ===")
user_b_order = {
    "id": "ord_test_user_b",
    "token": "#C-12",
    "userId": "usr_" + user_b_phone,
    "user_id": "usr_" + user_b_phone,
    "customer": "Priya Patel",
    "customerName": "Priya Patel",
    "customer_name": "Priya Patel",
    "customerPhone": user_b_phone,
    "customer_phone": user_b_phone,
    "customerYear": "Sem 6 • 3rd Year",
    "items": [{"dishId": "masala_dosa", "name": "Crispy Masala Dosa", "qty": 1, "price": 60}],
    "total": 60,
    "time": "01:00 PM",
    "arrivalTime": "01:10 PM",
    "arrival_time": "01:10 PM",
    "arrivalMinutes": 10,
    "arrival_minutes": 10,
    "status": "Cooking"
}
status, order_b_res = post("/api/orders", user_b_order)
assert status in (200, 201)

status, user_b_orders = get(f"/api/orders?phone={user_b_phone}")
assert len(user_b_orders.get("orders", [])) == 1, "User B should now see exactly 1 order"
print(f"✓ User B sees exactly their own order: Token {user_b_orders['orders'][0]['token']} for {user_b_orders['orders'][0]['customer_name']}")

print("\n=== 7. TEST USER A CAN FETCH ONLY USER A's ORDERS ===")
status, user_a_orders = get(f"/api/orders?phone={user_a_phone}")
orders_a = user_a_orders.get("orders", [])
print(f"User A (Phone {user_a_phone}) fetched orders count: {len(orders_a)}")
assert len(orders_a) >= 1
for ord in orders_a:
    assert ord["customer_phone"] == user_a_phone, "User A received someone else's order!"
    print(f"  • Token: {ord['token']} | Customer: {ord['customer_name']} | Phone: {ord['customer_phone']} | Arrival: {ord.get('arrival_time')}")

print("\n=== ALL WORKFLOW TESTS PASSED CLEANLY WITH ZERO ERRORS! ===")
