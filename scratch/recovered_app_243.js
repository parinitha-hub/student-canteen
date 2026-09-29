import urllib.request
import json

base = 'http://127.0.0.1:5000'

# 1. Test GET /
with urllib.request.urlopen(f'{base}/') as r:
    assert r.status == 200
    html = r.read().decode('utf-8')
    assert 'btn-top-login' in html
    assert 'View Food Menu &amp; Order' in html
    assert 'btn-hero-order-now' in html
    assert 'value="Student"' not in html
    assert 'value="9876543210"' not in html
    print('[PASS] GET / HTML is clean and properly configured')

# 2. Test GET /js/app.js
with urllib.request.urlopen(f'{base}/js/app.js') as r:
    assert r.status == 200
    js = r.read().decode('utf-8')
    assert 'btn-order-now-selected' in js
    assert 'openCartModal' in js
    assert 'cleanPhone = "9876543210"' not in js
    print('[PASS] GET /js/app.js contains Order Now logic and no fake phone numbers')

# 3. Test GET /css/style.css
with urllib.request.urlopen(f'{base}/css/style.css') as r:
    assert r.status == 200
    css = r.read().decode('utf-8')
    assert '.cart-floating-bar' in css
    assert '.btn-order-now-selected' in css
    print('[PASS] GET /css/style.css contains floating bar and Order Now styling')

# 4. Test POST /api/orders (live order placement)
order_payload = {
    'id': 'ORD-9999',
    'token': '#T-99',
    'customerName': 'Srinath',
    'customerYear': '3rd Year',
    'customerPhone': '',
    'items': [{'id': 'veg_biryani', 'name': 'Veg Biryani', 'qty': 1, 'price': 110, 'subtotal': 110}],
    'total': 110,
    'time': '12:00 PM',
    'status': 'Preparing in Kitchen ⏳',
    'timestamp': 1789999999999
}

req = urllib.request.Request(f'{base}/api/orders', data=json.dumps(order_payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    assert r.status == 201
    res = json.loads(r.read().decode('utf-8'))
    assert res['status'] == 'success'
    print('[PASS] POST /api/orders successfully placed order without fake phone numbers')

# 5. Test GET /api/orders
with urllib.request.urlopen(f'{base}/api/orders') as r:
    assert r.status == 200
    res = json.loads(r.read().decode('utf-8'))
    orders = res['orders']
    assert any(o['customerName'] == 'Srinath' for o in orders)
    assert not any(o['customerPhone'] == '9876543210' for o in orders)
    print(f'[PASS] GET /api/orders returns live orders without mock data: {[o["customerName"] for o in orders]}')

# Clean up test order
req_del = urllib.request.Request(f'{base}/api/orders/ORD-9999', method='DELETE')
with urllib.request.urlopen(req_del) as r:
    assert r.status == 200
    print('[PASS] Cleaned up test order successfully')

print('\nALL SERVER AND API TESTS COMPLETED 100% SUCCESSFULLY!')
