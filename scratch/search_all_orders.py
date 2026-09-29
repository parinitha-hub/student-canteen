import os
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['.git', 'scratch', '__pycache__']):
        continue
    for f in files:
        if f.endswith(('.js', '.html')):
            p = os.path.join(root, f)
            try:
                for i, l in enumerate(open(p, encoding='utf-8', errors='ignore')):
                    if any(k in l for k in ['myOrders', 'liveOrders', 'token-modal', 'savitha_student_active_order', 'live-order']):
                        print(f"{p}:{i+1}:{l.strip()[:80]}")
            except Exception as e:
                pass
