import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from backend.app import app

client = app.test_client()

routes_to_test = [
    ("/", "GET", None, 200),
    ("/css/style.css", "GET", None, 200),
    ("/js/app.js", "GET", None, 200),
    ("/js/charts.js", "GET", None, 200),
    ("/js/model_engine.js", "GET", None, 200),
    ("/assets/logo.png", "GET", None, 200),
    ("/assets/favicon.png", "GET", None, 200),
    ("/assets/hero_banner.jpg", "GET", None, 200),
    ("/api/health", "GET", None, 200),
    ("/api/analytics", "GET", None, 200),
    ("/api/history", "GET", None, 200),
    ("/api/feedback", "GET", None, 200),
    ("/api/orders", "GET", None, 200),
]

all_passed = True
print("Testing Flask endpoints...")
for url, method, body, expected_status in routes_to_test:
    if method == "GET":
        res = client.get(url)
    elif method == "POST":
        res = client.post(url, data=json.dumps(body), content_type="application/json")
    
    if res.status_code == expected_status:
        print(f" [PASS] {method} {url} -> {res.status_code}")
    else:
        print(f" [FAIL] {method} {url} -> Expected {expected_status}, got {res.status_code}")
        all_passed = False

# Test POST /api/predict
predict_payload = {
    "food_item": "Veg Biryani",
    "day_of_week": "Friday",
    "weather": "Sunny",
    "is_holiday": 0,
    "special_event": "None",
    "previous_day_sales": 140,
    "previous_week_sales": 135
}
res = client.post("/api/predict", data=json.dumps(predict_payload), content_type="application/json")
if res.status_code == 200:
    data = res.get_json()
    print(f" [PASS] POST /api/predict -> 200 (Predicted: {data.get('predicted_quantity')}, Portions: {data.get('recommended_portions')})")
else:
    print(f" [FAIL] POST /api/predict -> {res.status_code}: {res.data}")
    all_passed = False

# Test POST /api/predict_all
res = client.post("/api/predict_all", data=json.dumps({"day_of_week": "Monday", "weather": "Sunny", "is_holiday": 0, "special_event": "None"}), content_type="application/json")
if res.status_code == 200:
    data = res.get_json()
    print(f" [PASS] POST /api/predict_all -> 200 (Items predicted: {len(data.get('predictions', []))})")
else:
    print(f" [FAIL] POST /api/predict_all -> {res.status_code}: {res.data}")
    all_passed = False

# Test POST /api/orders
order_payload = {
    "token": "TEST-01",
    "customer_name": "Test User",
    "customer_year": "2nd Year",
    "customer_phone": "9876543210",
    "items": [{"name": "Veg Biryani", "price": 110, "qty": 1}],
    "total": 110
}
res = client.post("/api/orders", data=json.dumps(order_payload), content_type="application/json")
if res.status_code in [200, 201]:
    print(f" [PASS] POST /api/orders -> {res.status_code}")
else:
    print(f" [FAIL] POST /api/orders -> {res.status_code}: {res.data}")
    all_passed = False

# Test POST /api/feedback
fb_payload = {
    "name": "Test Student",
    "year": "1st Year",
    "rating": 5,
    "category": "Food Quality",
    "comment": "Delicious food and super fast ordering!"
}
res = client.post("/api/feedback", data=json.dumps(fb_payload), content_type="application/json")
if res.status_code in [200, 201]:
    print(f" [PASS] POST /api/feedback -> {res.status_code}")
else:
    print(f" [FAIL] POST /api/feedback -> {res.status_code}: {res.data}")
    all_passed = False

print("\nResult:", "ALL ENDPOINTS WORKING PERFECTLY!" if all_passed else "SOME ENDPOINTS FAILED!")
