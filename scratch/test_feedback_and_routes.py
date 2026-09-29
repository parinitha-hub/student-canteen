import os
import sys
import json
import urllib.request
import urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

def test_static_html():
    print("=== Testing HTML & Static Content ===")
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    assert "Parinitha.S" in html, "Parinitha.S developer credit missing in index.html"
    assert "about-website" in html, "about-website section missing in index.html"
    assert "feedback-section" in html, "feedback-section missing in index.html"
    assert "btn-top-login" in html, "btn-top-login missing in index.html"
    assert 'id="view-order" style="display:block;"' in html, "Homepage (view-order) is not open by default"
    assert 'id="view-login" class="login-screen-wrap" style="display:none;"' in html, "Login portal is not hidden by default"
    print("[PASS] index.html content assertions verified successfully!")

    with open(os.path.join(ROOT, "frontend", "index.html"), "r", encoding="utf-8") as f:
        f_html = f.read()
    assert "Parinitha.S" in f_html, "Parinitha.S missing in frontend/index.html"
    assert "about-website" in f_html, "about-website missing in frontend/index.html"
    assert "feedback-section" in f_html, "feedback-section missing in frontend/index.html"
    print("[PASS] frontend/index.html content assertions verified successfully!")

    with open(os.path.join(ROOT, "js", "app.js"), "r", encoding="utf-8") as f:
        js = f.read()
    assert "handleFeedbackSubmit" in js, "handleFeedbackSubmit missing in js/app.js"
    assert "navigateToSection" in js, "navigateToSection missing in js/app.js"
    assert "loadFeedback" in js, "loadFeedback missing in js/app.js"
    print("[PASS] js/app.js feedback and navigation functions verified successfully!")

def test_flask_app():
    print("\n=== Testing Flask Application & Feedback Endpoints ===")
    from backend.app import app
    client = app.test_client()

    # Test root endpoint
    res = client.get("/")
    assert res.status_code == 200, f"Root returned status {res.status_code}"
    html_text = res.get_data(as_text=True)
    assert "Parinitha.S" in html_text, "Parinitha.S not found in served root HTML"
    assert "Savitha" in html_text, "Savitha not found in served root HTML"
    print("[PASS] GET / -> HTTP 200 with Parinitha.S credit")

    # Test health
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    print(f"[PASS] GET /api/health -> HTTP 200 (Model loaded: {data['model_loaded']})")

    # Test get feedback
    res = client.get("/api/feedback")
    assert res.status_code == 200
    fb_data = res.get_json()
    assert fb_data["status"] == "success"
    assert len(fb_data["feedback"]) >= 3
    print(f"[PASS] GET /api/feedback -> HTTP 200 ({len(fb_data['feedback'])} reviews returned)")

    # Test post feedback
    new_fb = {
        "name": "Divya Sharma",
        "year": "3rd Year AI & DS",
        "rating": 5,
        "category": "Website Experience",
        "comment": "Outstanding platform created by Parinitha.S! Ordering lunch takes literally 10 seconds."
    }
    res = client.post("/api/feedback", data=json.dumps(new_fb), content_type="application/json")
    assert res.status_code == 201
    post_data = res.get_json()
    assert post_data["status"] == "success"
    assert post_data["feedback"]["name"] == "Divya Sharma"
    print("[PASS] POST /api/feedback -> HTTP 201 created successfully")

    # Re-verify feedback count increased
    res = client.get("/api/feedback")
    fb_data_after = res.get_json()
    names = [f["name"] for f in fb_data_after["feedback"]]
    assert "Divya Sharma" in names
    print(f"[PASS] Verified new feedback is persisted in SQLite! Total reviews: {len(fb_data_after['feedback'])}")

    print("\n>>> ALL TESTS PASSED WITH 0 ERRORS! <<<")

if __name__ == "__main__":
    test_static_html()
    test_flask_app()
