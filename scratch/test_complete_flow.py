import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(url, method="GET", data=None):
    req = urllib.request.Request(url, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
    with urllib.request.urlopen(req, data=body, timeout=5) as resp:
        return resp.status, resp.read().decode("utf-8")

def main():
    print("=== Running Comprehensive Verification Test ===")
    
    # 1. Test Root / (HTML)
    status, html = test_endpoint(f"{BASE_URL}/")
    assert status == 200, f"Expected 200, got {status}"
    print("[PASS] GET / returns 200 OK")
    
    # Check elements in HTML
    assert 'id="view-about"' in html, "Missing #view-about"
    assert 'id="view-login"' in html, "Missing #view-login"
    assert 'id="view-order"' in html, "Missing #view-order"
    assert 'id="view-manager"' in html, "Missing #view-manager"
    assert 'Parinitha.S' in html, "Developer Parinitha.S not found in HTML"
    assert 'btn-top-login' in html, "Missing btn-top-login"
    assert 'btn-back-about' in html, "Missing btn-back-about"
    assert 'feedback-section' in html, "Missing feedback-section"
    header_chunk = html.split('<header>')[1].split('</header>')[0]
    assert 'btn-top-login' in header_chunk, "Login button not found in navigation bar"
    assert 'nav-btn-about' not in header_chunk, "Navigation bar should not contain extra nav-btn-about"
    assert 'nav-btn-home' not in header_chunk, "Navigation bar should not contain extra nav-btn-home"
    assert 'nav-btn-kitchen' not in header_chunk, "Navigation bar should not contain extra nav-btn-kitchen"
    print("[PASS] Navigation bar contains ONLY Login, and no other tabs!")

    # 2. Test CSS
    status, css = test_endpoint(f"{BASE_URL}/css/style.css")
    assert status == 200, f"Expected 200 for CSS, got {status}"
    assert '.login-screen-wrap' in css, "Missing .login-screen-wrap in CSS"
    assert '.btn-top-login' in css, "Missing .btn-top-login in CSS"
    assert '.btn-back-about' in css, "Missing .btn-back-about in CSS"
    assert '.developer-spotlight-card' in css, "Missing .developer-spotlight-card in CSS"
    assert '.feedback-section' in css, "Missing .feedback-section in CSS"
    print("[PASS] CSS served correctly and contains all modern styling classes")

    # 3. Test JS
    status, js = test_endpoint(f"{BASE_URL}/js/app.js")
    assert status == 200, f"Expected 200 for JS, got {status}"
    assert 'performSwitchMode("about")' in js, "Missing performSwitchMode('about') in initUserAuth"
    assert 'mode === "about"' in js, "Missing mode === 'about' in performSwitchMode"
    assert 'mode === "login"' in js, "Missing mode === 'login' in performSwitchMode"
    assert 'target === "about"' in js, "Missing target === 'about' in navigateToSection"
    assert 'target === "login"' in js, "Missing target === 'login' in navigateToSection"
    assert 'window.performSwitchMode = performSwitchMode;' in js, "Missing window.performSwitchMode export"
    print("[PASS] JS contains accurate About and Login page toggling and window bindings")

    # 4. Test API Health
    status, health_body = test_endpoint(f"{BASE_URL}/api/health")
    assert status == 200, f"Expected 200 for health, got {status}"
    health_data = json.loads(health_body)
    assert health_data.get("status") == "healthy", f"Health status not healthy: {health_data}"
    print(f"[PASS] Health check: {health_data.get('algorithm')} online!")

    # 5. Test Feedback GET
    status, fb_body = test_endpoint(f"{BASE_URL}/api/feedback")
    assert status == 200, f"Expected 200 for feedback GET, got {status}"
    fb_data = json.loads(fb_body)
    fb_list = fb_data.get("feedback", [])
    assert isinstance(fb_list, list), "Feedback should be a list"
    assert len(fb_list) >= 3, f"Expected at least 3 reviews, got {len(fb_list)}"
    print(f"[PASS] GET /api/feedback returned {len(fb_list)} verified reviews")

    # 6. Test Feedback POST
    test_review = {
        "name": "Arun Kumar",
        "year": "3rd Year AI & DS",
        "rating": 5,
        "category": "Website Experience",
        "comment": "Incredible work by Parinitha.S! The about page and zero-wait tokens are revolutionary."
    }
    status, fb_post_body = test_endpoint(f"{BASE_URL}/api/feedback", method="POST", data=test_review)
    assert status == 201, f"Expected 201 for feedback POST, got {status}"
    fb_resp = json.loads(fb_post_body)
    assert fb_resp.get("status") == "success", f"Feedback POST failed: {fb_resp}"
    print("[PASS] POST /api/feedback created review successfully")

    # 7. Test AI Prediction
    pred_payload = {
        "food_item": "Veg Biryani",
        "day_of_week": "Friday",
        "weather": "Rainy",
        "special_event": "Tech Symposium",
        "is_holiday": 0,
        "previous_day_sales": 180,
        "previous_week_sales": 175
    }
    status, pred_body = test_endpoint(f"{BASE_URL}/api/predict", method="POST", data=pred_payload)
    assert status == 200, f"Expected 200 for prediction, got {status}"
    pred_data = json.loads(pred_body)
    assert "predicted_quantity" in pred_data and "recommended_portions" in pred_data, f"Invalid prediction: {pred_data}"
    print(f"[PASS] AI Prediction: {pred_data.get('input_data', {}).get('food_item')} -> {pred_data.get('predicted_quantity')} portions (Recommended: {pred_data.get('recommended_portions')})")

    print("\nALL VERIFICATIONS PASSED WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
