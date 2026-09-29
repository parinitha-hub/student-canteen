import sys
sys.stdout.reconfigure(encoding='utf-8')

markers = [
    "view-about",
    "reviews-section",
    "reviews-cards-grid",
    "view-login",
    "login-student-name",
    "view-order",
    "dishes-grid",
    "my-orders-modal",
    "assets/parinitha.jpg",
    "Connect on LinkedIn"
]

text = open("index.html", encoding="utf-8").read()
print("Checking index.html markers:")
all_found = True
for m in markers:
    found = m in text
    print(f" - {m}: {found}")
    if not found:
        all_found = False

print("\nAll markers present:", all_found)
