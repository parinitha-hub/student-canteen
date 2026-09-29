with open('scratch/build_clean_app_js.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = """  try {
    Object.defineProperty(window, "myOrders", {
      get: () => myOrders,
      set: (v) => { myOrders = v; },
      configurable: true
    });
  } catch (e) {
    window.myOrders = myOrders;
  }
}"""

replacement = """  try {
    Object.defineProperty(window, "myOrders", {
      get: () => myOrders,
      set: (v) => { myOrders = v; },
      configurable: true
    });
  } catch (e) {
    window.myOrders = myOrders;
  }

  try {
    Object.defineProperty(window, "cart", {
      get: () => cart,
      set: (v) => { cart = v; },
      configurable: true
    });
  } catch (e) {
    window.cart = cart;
  }

  try {
    Object.defineProperty(window, "lastPlacedOrder", {
      get: () => lastPlacedOrder,
      set: (v) => { lastPlacedOrder = v; },
      configurable: true
    });
  } catch (e) {
    window.lastPlacedOrder = lastPlacedOrder;
  }
}"""

if target in c:
    c = c.replace(target, replacement, 1)
    with open('scratch/build_clean_app_js.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Updated scratch/build_clean_app_js.py")
else:
    print("TARGET NOT FOUND")
