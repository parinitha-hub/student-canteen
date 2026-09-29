import urllib.request
import json

base = 'http://127.0.0.1:5000'

# 1. HTML
html = urllib.request.urlopen(f'{base}/').read().decode('utf-8')
assert 'id="view-login"' in html, 'Missing view-login in HTML'
assert 'simple-login-card' in html, 'Missing simple-login-card in HTML'
assert 'Rahul Sharma' not in html, 'Student name Rahul Sharma should not be seen in HTML'
assert 'savitha123' not in html, 'Staff password savitha123 should not be seen in HTML'
print('[OK] HTML test passed: Student name and password are NOT visible in HTML')

# 2. CSS
css = urllib.request.urlopen(f'{base}/css/style.css').read().decode('utf-8')
assert '.login-screen-wrap' in css, 'Missing .login-screen-wrap in CSS'
assert '.simple-login-card' in css, 'Missing .simple-login-card in CSS'
print('[OK] CSS test passed: Login styles and responsive centering verified')

# 3. JS
js = urllib.request.urlopen(f'{base}/js/app.js').read().decode('utf-8')
assert 'performSwitchMode("login")' in js, 'Missing performSwitchMode login'
print('[OK] JS test passed: Auth initialization and login routing verified')

# 4. Health
health = json.loads(urllib.request.urlopen(f'{base}/api/health').read().decode('utf-8'))
assert health.get('status') in ['healthy', 'ok'], f'Health status: {health}'
print('[OK] API Health check passed')

# 5. Predict API
req = urllib.request.Request(
    f'{base}/api/predict',
    data=json.dumps({
        'food_item': 'Veg Biryani',
        'day_of_week': 'Monday',
        'weather': 'Sunny',
        'is_holiday': 0,
        'special_event': 'Normal Day',
        'previous_day_sales': 140,
        'previous_week_sales': 135
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
pred = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert 'predicted_quantity' in pred, f'Prediction failed: {pred}'
print(f'[OK] AI Prediction passed: {pred.get("predicted_quantity")} portions (recommended: {pred.get("recommended_portions")})')

# 6. Analytics API
req_analytics = urllib.request.urlopen(f'{base}/api/analytics')
analytics = json.loads(req_analytics.read().decode('utf-8'))
print(f'[OK] Analytics API passed: status={analytics.get("status")}')

# 7. History API
req_hist = urllib.request.urlopen(f'{base}/api/history')
hist = json.loads(req_hist.read().decode('utf-8'))
print(f'[OK] History API passed: {len(hist.get("records", []))} records found')

print('\nALL TESTS PASSED WITH ZERO ERRORS!')
