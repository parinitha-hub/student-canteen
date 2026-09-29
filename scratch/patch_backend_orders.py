with open('backend/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            orders.append({
                "id": d["id"],
                "token": d["token"],
                "customerName": d["customer_name"],
                "customerYear": d["customer_year"],
                "customerPhone": d["customer_phone"],
                "items": items_list,
                "total": d["total"],
                "time": d["time"],
                "status": d["status"],
                "timestamp": d["timestamp"]
            })'''

replacement1 = '''            orders.append({
                "id": d["id"],
                "token": d["token"],
                "customer": d["customer_name"],
                "customerName": d["customer_name"],
                "customer_name": d["customer_name"],
                "customerYear": d["customer_year"],
                "customer_year": d["customer_year"],
                "customerPhone": d["customer_phone"],
                "customer_phone": d["customer_phone"],
                "items": items_list,
                "total": d["total"],
                "time": d["time"],
                "status": d["status"],
                "timestamp": d["timestamp"]
            })'''

target2 = 'cust_name = data.get("customerName") or data.get("customer_name") or "Student"'
replacement2 = 'cust_name = data.get("customer") or data.get("customerName") or data.get("customer_name") or "Student"'

target3 = 'cust_year = data.get("customerYear") or data.get("customer_year") or "1st Year"'
replacement3 = 'cust_year = data.get("customerYear") or data.get("customer_year") or data.get("year") or "1st Year"'

target4 = 'cust_phone = data.get("customerPhone") or data.get("customer_phone") or ""'
replacement4 = 'cust_phone = data.get("customerPhone") or data.get("customer_phone") or data.get("phone") or ""'

if target1 in text and target2 in text:
    text = text.replace(target1, replacement1, 1)
    text = text.replace(target2, replacement2, 1)
    text = text.replace(target3, replacement3, 1)
    text = text.replace(target4, replacement4, 1)
    with open('backend/app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated backend/app.py with student customer names!")
else:
    print("ERROR: Targets not found in backend/app.py")
