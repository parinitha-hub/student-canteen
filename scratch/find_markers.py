with open('index.html', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        for term in ['subtab-orders-btn', 'manager-pane-orders', 'manager-pane-calc', 'id="cart-modal"', 'id="my-orders-modal"']:
            if term in line:
                print(f'{term} at line {i}')
