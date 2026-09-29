import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Testing http://127.0.0.1:5000 endpoints...")

# 1. Health API
try:
    res = urllib.request.urlopen('http://127.0.0.1:5000/api/health')
    print("Health API status:", res.status)
    data = json.loads(res.read().decode('utf-8'))
    print("Health API data:", data)
except Exception as e:
    print("Health API failed:", e)

# 2. Orders GET API
try:
    res = urllib.request.urlopen('http://127.0.0.1:5000/api/orders')
    print("Orders API status:", res.status)
    data = json.loads(res.read().decode('utf-8'))
    print("Orders count:", data.get('count'))
except Exception as e:
    print("Orders API failed:", e)

# 3. Orders POST API (placing a test order)
try:
    req_data = json.dumps({
        "id": "ord_test_verification",
        "token": "#A-88",
        "customer": "Test Student",
        "customerYear": "2nd Year",
        "items": [{"dishId": "veg_biryani", "name": "Veg Biryani", "qty": 1, "price": 110}],
        "total": 110,
        "time": "08:15 PM",
        "status": "Preparing in Kitchen ⏳",
        "timestamp": 1234567890
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5000/api/orders', data=req_data, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    print("Create Order API status:", res.status)
    post_res = json.loads(res.read().decode('utf-8'))
    print("Order created:", post_res.get('status'), post_res.get('order', {}).get('token'))

    # Clean up test order
    req_del = urllib.request.Request('http://127.0.0.1:5000/api/orders/ord_test_verification', method='DELETE')
    res_del = urllib.request.urlopen(req_del)
    print("Cancel Order API status:", res_del.status)
except Exception as e:
    print("Orders POST API failed:", e)

# 4. Root HTML verification
try:
    res_root = urllib.request.urlopen('http://127.0.0.1:5000/')
    html = res_root.read().decode('utf-8')
    print("\nRoot HTML Verification:")
    print(" - Total length:", len(html), "bytes")
    print(" - gov-top-bar present:", 'gov-top-bar' in html, "(Expected: False)")
    print(" - official-announcement-bar present:", 'official-announcement-bar' in html, "(Expected: False)")
    print(" - nav-btn-home display none:", 'id="nav-btn-home"' in html and 'style="display:none;"' in html, "(Expected: True)")
    print(" - btn-top-my-orders-nav display none:", 'id="btn-top-my-orders-nav"' in html and 'style="display:none;"' in html, "(Expected: True)")
    print(" - view-about present:", 'id="view-about"' in html, "(Expected: True)")
    print(" - How It Works present:", 'How Savitha Canteen Works' in html, "(Expected: True)")
    print(" - Developer Parinitha.S present:", 'Parinitha.S' in html, "(Expected: True)")
    print(" - My Orders Modal present:", 'id="my-orders-modal"' in html, "(Expected: True)")
except Exception as e:
    print("Root HTML fetch failed:", e)
