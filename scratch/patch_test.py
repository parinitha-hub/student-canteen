with open('scratch/test_order_now_flow.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("elements['my-orders-list']", "elements['my-orders-list-container']")

with open('scratch/test_order_now_flow.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated test script!")
