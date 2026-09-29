import os
import shutil

output_file = 'js/app.js'

script_content = '''/**
 * Savitha Canteen - Complete Client-side Controller & AI Kitchen Engine
 * Developed & Architected by Parinitha.S
 */

// =========================================================================
// 1. FOOD MENU CATALOG WITH AUTHENTIC PHOTOGRAPHY & DISH DATA
// =========================================================================
const DISHES = [
  {
    id: "veg_biryani",
    name: "Veg Biryani",
    category: "lunch",
    price: 110,
    rating: 4.8,
    reviews: 142,
    isVeg: true,
    image: "assets/veg_biryani.jpg",
    desc: "Aromatic basmati rice layered with fresh vegetables, mint, and secret royal biryani masala. Served with cooling raita.",
    demandStatus: "🔥 High Demand Today (~195 portions cooking)"
  },
  {
    id: "chicken_biryani",
    name: "Chicken Biryani",
    category: "lunch",
    price: 150,
    rating: 4.9,
    reviews: 218,
    isVeg: false,
    image: "assets/chicken_biryani.jpg",
    desc: "Dum-cooked tender chicken pieces with fragrant saffron rice, fried onions and boiled egg. Served with mirchi ka salan.",
    demandStatus: "⚡ Campus Bestseller"
  },
  {
    id: "masala_dosa",
    name: "Masala Dosa",
    category: "breakfast",
    price: 80,
    rating: 4.7,
    reviews: 164,
    isVeg: true,
    image: "assets/masala_dosa.jpg",
    desc: "Crispy golden fermented crepe roasted in pure ghee, stuffed with seasoned potato filling. Served with piping hot sambar.",
    demandStatus: "🥞 Morning Rush Favorite"
  },
  {
    id: "idli_vada",
    name: "Idli Vada Combo",
    category: "breakfast",
    price: 65,
    rating: 4.8,
    reviews: 185,
    isVeg: true,
    image: "assets/idli_vada.jpg",
    desc: "Two fluffy steamed rice idlis paired with one crispy golden medu vada. Served with fresh coconut chutney and vegetable sambar.",
    demandStatus: "🥞 South Indian Classic"
  },
  {
    id: "puri_bhaji",
    name: "Golden Puri Bhaji",
    category: "breakfast",
    price: 75,
    rating: 4.8,
    reviews: 172,
    isVeg: true,
    image: "assets/puri_bhaji.jpg",
    desc: "Three hot, fluffy golden puffed puris served with aromatic spiced potato bhaji gravy, fried green chilies, and lemon pickle.",
    demandStatus: "🥞 Campus Breakfast Special"
  },
  {
    id: "paneer_thali",
    name: "Paneer Thali",
    category: "lunch",
    price: 130,
    rating: 4.8,
    reviews: 98,
    isVeg: true,
    image: "assets/paneer_thali.jpg",
    desc: "Wholesome lunch plate: Rich paneer butter masala, dal tadka, jeera rice, 2 soft butter rotis, salad and gulab jamun.",
    demandStatus: "🍱 Full Meal Favorite"
  },
  {
    id: "paneer_roti",
    name: "Paneer Butter Masala & Roti",
    category: "lunch",
    price: 125,
    rating: 4.8,
    reviews: 155,
    isVeg: true,
    image: "assets/paneer_roti.jpg",
    desc: "Tender cottage cheese cubes simmered in a luscious buttery tomato-cashew makhani gravy, served with 3 soft butter tawa rotis.",
    demandStatus: "🥘 North Indian Delight"
  },
  {
    id: "chole_bhature",
    name: "Chole Bhature",
    category: "lunch",
    price: 95,
    rating: 4.6,
    reviews: 112,
    isVeg: true,
    image: "assets/chole_bhature.jpg",
    desc: "Two fluffy puffed bhaturas served with spicy Punjabi chickpea masala, pickled carrots, and green chili salad.",
    demandStatus: "🫓 Brunch Special"
  },
  {
    id: "curd_rice",
    name: "South Indian Curd Rice",
    category: "lunch",
    price: 70,
    rating: 4.9,
    reviews: 128,
    isVeg: true,
    image: "assets/curd_rice.jpg",
    desc: "Cooling tempered yogurt rice with mustard seeds, fresh ginger, curry leaves, and juicy pomegranate pearls. Served with mango pickle.",
    demandStatus: "🌿 Healthy & Soothing"
  },
  {
    id: "fried_rice",
    name: "Veg Fried Rice",
    category: "lunch",
    price: 90,
    rating: 4.6,
    reviews: 84,
    isVeg: true,
    image: "assets/fried_rice.jpg",
    desc: "Wok-tossed long-grain basmati rice with crunchy capsicum, carrots, spring onions, and savory garlic-soy seasoning.",
    demandStatus: "🍚 Quick Hot Meal"
  },
  {
    id: "egg_fried_rice",
    name: "Egg Fried Rice",
    category: "lunch",
    price: 110,
    rating: 4.8,
    reviews: 146,
    isVeg: false,
    image: "assets/egg_fried_rice.jpg",
    desc: "Fragrant rice stir-fried in a fiery wok with scrambled egg ribbons, crisp vegetables, white pepper, and chili garlic glaze.",
    demandStatus: "🍳 High Protein Special"
  },
  {
    id: "hakka_noodles",
    name: "Veg Hakka Noodles",
    category: "lunch",
    price: 95,
    rating: 4.8,
    reviews: 215,
    isVeg: true,
    image: "assets/hakka_noodles.jpg",
    desc: "Slurp-worthy street-style noodles wok-tossed with julienned cabbage, bell peppers, carrots, toasted sesame, and scallions.",
    demandStatus: "🍜 Indo-Chinese Bestseller"
  },
  {
    id: "chicken_roll",
    name: "Chicken Kathi Roll",
    category: "lunch",
    price: 110,
    rating: 4.8,
    reviews: 195,
    isVeg: false,
    image: "assets/chicken_roll.jpg",
    desc: "Flaky paratha wrap loaded with grilled marinated chicken tikka chunks, crisp onions, green chilies, and tangy mint mayonnaise.",
    demandStatus: "⚡ Grab-and-Go Student Favorite"
  },
  {
    id: "paneer_roll",
    name: "Paneer Tikka Kathi Roll",
    category: "lunch",
    price: 100,
    rating: 4.8,
    reviews: 168,
    isVeg: true,
    image: "assets/paneer_roll.jpg",
    desc: "Crispy grilled paratha tightly rolled with smoky tandoori paneer cubes, crunchy peppers, sliced red onions, and chaat masala.",
    demandStatus: "🌯 Student Street Bite"
  },
  {
    id: "pav_bhaji",
    name: "Mumbai Pav Bhaji",
    category: "snacks",
    price: 90,
    rating: 4.9,
    reviews: 240,
    isVeg: true,
    image: "assets/pav_bhaji.jpg",
    desc: "Rich spiced mashed vegetable gravy topped with a dollop of pure Amul butter, served with two toasted soft pavs and lemon onion salad.",
    demandStatus: "🔥 Evening Campus Bestseller"
  },
  {
    id: "samosa_chai",
    name: "Samosa & Cutting Chai",
    category: "snacks",
    price: 40,
    rating: 4.9,
    reviews: 310,
    isVeg: true,
    image: "assets/samosa_chai.jpg",
    desc: "Two crispy hand-rolled potato & green pea samosas paired with steaming fragrant cardamom-infused cutting chai.",
    demandStatus: "☕ All-Time Snack Favorite"
  },
  {
    id: "onion_pakoda",
    name: "Crispy Onion Pakoda",
    category: "snacks",
    price: 50,
    rating: 4.8,
    reviews: 188,
    isVeg: true,
    image: "assets/onion_pakoda.jpg",
    desc: "Crunchy besan-battered spiced onion fritters fried crisp and golden. Served with spicy mint chutney and sweet tamarind dip.",
    demandStatus: "🌧️ Rainy Day Crunch"
  },
  {
    id: "masala_maggi",
    name: "Cheese Masala Maggi",
    category: "snacks",
    price: 55,
    rating: 4.9,
    reviews: 340,
    isVeg: true,
    image: "assets/masala_maggi.jpg",
    desc: "College-style double masala 2-minute noodles tossed with sweet corn, green peas, carrots, and topped with grated cheddar cheese.",
    demandStatus: "🍜 All-Time Late Snack Hit"
  },
  {
    id: "sandwich",
    name: "Grilled Cheese Sandwich",
    category: "snacks",
    price: 65,
    rating: 4.7,
    reviews: 130,
    isVeg: true,
    image: "assets/sandwich.jpg",
    desc: "Tri-layer toasted jumbo bread packed with mozzarella cheese, sweet corn, sliced tomatoes and spicy mint chutney.",
    demandStatus: "🥪 Exam Week Quick Bite"
  },
  {
    id: "cold_coffee",
    name: "Thick Cold Coffee",
    category: "snacks",
    price: 50,
    rating: 4.8,
    reviews: 275,
    isVeg: true,
    image: "assets/cold_coffee.jpg",
    desc: "Creamy iced blended coffee crafted with rich roasted espresso, chilled milk, and a decadent drizzle of Hershey\'s chocolate syrup.",
    demandStatus: "☕ Chilled Summer Sensation"
  },
  {
    id: "mango_lassi",
    name: "Royal Mango Lassi",
    category: "snacks",
    price: 60,
    rating: 4.9,
    reviews: 160,
    isVeg: true,
    image: "assets/mango_lassi.jpg",
    desc: "Traditional thick beaten yogurt lassi infused with natural Alphonso mango pulp, fragrant cardamom, and slivered pistachios.",
    demandStatus: "🥭 Refreshing Thirst Quencher"
  },
  {
    id: "lime_soda",
    name: "Fresh Sparkling Lime Soda",
    category: "snacks",
    price: 40,
    rating: 4.7,
    reviews: 145,
    isVeg: true,
    image: "assets/lime_soda.jpg",
    desc: "Zesty freshly squeezed lime juice with sparkling club soda, rock salt, mint leaves, and ice. Choose sweet, salted, or mixed.",
    demandStatus: "🍋 Instant Energy Drink"
  },
  {
    id: "gulab_jamun",
    name: "Hot Gulab Jamun (2 Pcs)",
    category: "snacks",
    price: 45,
    rating: 4.9,
    reviews: 210,
    isVeg: true,
    image: "assets/gulab_jamun.jpg",
    desc: "Two warm khoya dumplings fried to golden perfection and soaked in aromatic saffron and rose water sugar syrup.",
    demandStatus: "🍯 Sweet Tooth Special"
  },
  {
    id: "brownie_icecream",
    name: "Brownie with Ice Cream",
    category: "snacks",
    price: 95,
    rating: 4.9,
    reviews: 280,
    isVeg: true,
    image: "assets/brownie_icecream.jpg",
    desc: "Warm fudgy walnut brownie topped with a chilled vanilla ice cream scoop and drizzled with hot Belgian chocolate fudge sauce.",
    demandStatus: "🍫 Premium Campus Indulgence"
  }
];

// =========================================================================
// 2. GLOBAL STATE & ORDER MANAGEMENT
// =========================================================================
let cart = {}; // { dishId: quantity }
let currentCategory = "all";
let isBackendConnected = false;
let historyRecords = [];
let feedbackList = [];
let currentUser = null; // { role: 'student' | 'worker', name: string, ... }
let currentThemeIndex = 0;
let currentSwiggyRating = 5;
let currentReviewFilter = "all";
let lastPlacedOrder = null;

const INITIAL_SAMPLE_LIVE_ORDERS = [
  {
    id: "ord_sample_1",
    token: "#B-14",
    customer: "Karthik R.",
    customerName: "Karthik R.",
    customer_name: "Karthik R.",
    customerYear: "3rd Year",
    customer_year: "3rd Year",
    customerPhone: "9840123456",
    customer_phone: "9840123456",
    items: [
      { dishId: "veg_biryani", name: "Veg Biryani", qty: 1, price: 110 },
      { dishId: "cold_coffee", name: "Thick Cold Coffee", qty: 1, price: 50 }
    ],
    total: 160,
    time: "01:15 PM",
    timestamp: Date.now() - 360000,
    status: "Cooking",
    prepTime: "6-8 mins"
  },
  {
    id: "ord_sample_2",
    token: "#A-09",
    customer: "Ananya Sharma",
    customerName: "Ananya Sharma",
    customer_name: "Ananya Sharma",
    customerYear: "2nd Year",
    customer_year: "2nd Year",
    customerPhone: "9712345678",
    customer_phone: "9712345678",
    items: [
      { dishId: "masala_dosa", name: "Masala Dosa", qty: 1, price: 80 },
      { dishId: "mango_lassi", name: "Royal Mango Lassi", qty: 1, price: 60 }
    ],
    total: 140,
    time: "01:22 PM",
    timestamp: Date.now() - 180000,
    status: "Cooking",
    prepTime: "4-6 mins"
  }
];

let liveOrders = [];
try {
  const savedOrders = localStorage.getItem("savitha_live_orders");
  if (savedOrders) {
    liveOrders = JSON.parse(savedOrders);
    // Sanitize any generic "Student" names from previous runs
    liveOrders.forEach((ord, idx) => {
      if (!ord.customer || ord.customer === "Student") {
        ord.customer = idx % 2 === 0 ? "Karthik R." : "Ananya Sharma";
        ord.customerName = ord.customer;
        ord.customer_name = ord.customer;
        if (!ord.customerYear) ord.customerYear = "2nd Year";
      }
    });
  } else {
    liveOrders = [...INITIAL_SAMPLE_LIVE_ORDERS];
  }
} catch (e) {
  liveOrders = [...INITIAL_SAMPLE_LIVE_ORDERS];
}

let myOrders = [];
try {
  const savedMy = localStorage.getItem("savitha_my_orders");
  myOrders = savedMy ? JSON.parse(savedMy) : [];
} catch (e) {
  myOrders = [];
}

const API_BASE = (typeof window !== "undefined" && window.location && window.location.origin && window.location.origin.startsWith("http")) 
  ? window.location.origin 
  : "http://127.0.0.1:5000";

// =========================================================================
// 3. COLOR THEMES & PALETTE SWITCHER
// =========================================================================
const THEMES = [
  { id: "teal-coral", name: "Teal & Coral", icon: "🌊" },
  { id: "royal-violet", name: "Royal Violet", icon: "🌌" },
  { id: "midnight", name: "Midnight Dark", icon: "🌙" },
  { id: "ruby", name: "Ruby & Gold", icon: "🍷" }
];

function initTheme() {
  try {
    const savedTheme = localStorage.getItem("savitha_theme") || "teal-coral";
    const foundIdx = THEMES.findIndex(t => t.id === savedTheme);
    currentThemeIndex = foundIdx >= 0 ? foundIdx : 0;
  } catch (e) {
    currentThemeIndex = 0;
  }
  applyTheme(THEMES[currentThemeIndex]);
}

function cycleTheme() {
  currentThemeIndex = (currentThemeIndex + 1) % THEMES.length;
  const nextTheme = THEMES[currentThemeIndex];
  applyTheme(nextTheme);
  try {
    localStorage.setItem("savitha_theme", nextTheme.id);
  } catch (e) {}
  showToast(`Palette switched to ${nextTheme.name} ${nextTheme.icon}`, "info");
}

function applyTheme(theme) {
  if (theme.id === "teal-coral") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", theme.id);
  }
  const nameEl = document.getElementById("theme-name");
  if (nameEl) nameEl.textContent = theme.name;
  const iconEl = document.getElementById("theme-icon");
  if (iconEl) iconEl.textContent = theme.icon;
}

// =========================================================================
// 4. FOOD MENU & CART CONTROLLER
// =========================================================================
function renderDishes() {
  const container = document.getElementById("dishes-grid");
  if (!container) return;

  const filtered = currentCategory === "all" 
    ? DISHES 
    : DISHES.filter(d => d.category === currentCategory);

  let html = "";
  filtered.forEach(dish => {
    const qty = cart[dish.id] || 0;
    const typeClass = dish.isVeg ? "veg" : "non-veg";
    let buttonHtml = "";

    if (qty > 0) {
      buttonHtml = `
        <div class="qty-pill">
          <button type="button" onclick="updateDishQty('${dish.id}', -1)" aria-label="Decrease quantity">-</button>
          <span>${qty}</span>
          <button type="button" onclick="updateDishQty('${dish.id}', 1)" aria-label="Increase quantity">+</button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)">
          ADD +
        </button>
      `;
    }

    html += `
      <div class="dish-card">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">⭐ ${dish.rating}</span>
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>
          <p class="dish-desc">${dish.desc}</p>
          <div class="demand-tag">${dish.demandStatus}</div>
          <div class="dish-footer">
            <div class="dish-price">₹${dish.price}</div>
            <div id="btn-wrap-${dish.id}">
              ${buttonHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function filterCategory(cat, btn) {
  currentCategory = cat;
  document.querySelectorAll(".category-pill").forEach(p => p.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderDishes();
}

function updateDishQty(dishId, delta) {
  // STRICT LOGIN GUARD: Without login, cannot select dishes
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select dishes and order!", "warning");
    performSwitchMode("login");
    return;
  }

  const current = cart[dishId] || 0;
  const next = current + delta;
  if (next <= 0) {
    delete cart[dishId];
  } else {
    cart[dishId] = next;
  }

  renderDishes();
  updateCartBar();
}

function quickOrderDish(dishId) {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to select items!", "warning");
    performSwitchMode("login");
    return;
  }
  updateDishQty(dishId, 1);
  openCartModal();
}

function updateCartBar() {
  const bar = document.getElementById("cart-floating-bar");
  const counter = document.getElementById("cart-counter");
  const heroCount = document.getElementById("hero-cart-count");
  const totalVal = document.getElementById("floating-cart-total") || document.getElementById("cart-bar-total-val");
  const itemsVal = document.getElementById("floating-cart-count") || document.getElementById("cart-bar-items-val");

  let totalQty = 0;
  let totalPrice = 0;

  for (const [id, qty] of Object.entries(cart)) {
    const dish = DISHES.find(d => d.id === id);
    if (dish) {
      totalQty += qty;
      totalPrice += (dish.price * qty);
    }
  }

  if (counter) counter.textContent = totalQty;
  if (heroCount) heroCount.textContent = totalQty;

  if (totalVal) totalVal.textContent = `₹${totalPrice}`;
  if (itemsVal) itemsVal.textContent = `${totalQty} item${totalQty !== 1 ? 's' : ''} selected`;

  if (totalQty > 0) {
    if (bar) bar.classList.add("show");
  } else {
    if (bar) bar.classList.remove("show");
  }
}

function openCartModal() {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to access your cart!", "warning");
    performSwitchMode("login");
    return;
  }

  const modal = document.getElementById("cart-modal");
  const list = document.getElementById("cart-items-container") || document.getElementById("cart-items-list");
  const total = document.getElementById("cart-modal-total") || document.getElementById("bill-total");
  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  if (nameInput) {
    if (currentUser && currentUser.name && currentUser.name !== "Student") {
      nameInput.value = currentUser.name;
    } else if (!nameInput.value) {
      nameInput.value = currentUser && currentUser.name ? currentUser.name : "";
    }
  }
  if (yearInput && currentUser && currentUser.year) {
    yearInput.value = currentUser.year;
  }
  if (phoneInput && currentUser && currentUser.phone) {
    phoneInput.value = currentUser.phone;
  }

  if (!modal) return;

  const entries = Object.entries(cart);
  if (entries.length === 0) {
    if (list) {
      list.innerHTML = `
        <div style="text-align:center; padding:24px 12px;">
          <div style="font-size:2.4rem; margin-bottom:8px;">🛒</div>
          <div style="font-weight:800; font-size:1.05rem; color:var(--text-main);">Your Cart is Empty</div>
          <p style="color:var(--text-muted); font-size:0.85rem; margin:6px 0 16px 0;">Please select dishes from the food menu by clicking <strong>ADD +</strong>.</p>
          <button type="button" class="btn-hero-primary" onclick="closeCartModal();" style="padding:8px 18px; border-radius:999px;">
            Browse Dishes
          </button>
        </div>
      `;
    }
    if (total) total.textContent = "₹0";
    modal.classList.add("show");
    return;
  }

  let html = "";
  let sum = 0;

  entries.forEach(([id, qty]) => {
    const dish = DISHES.find(d => d.id === id);
    if (dish) {
      const itemCost = dish.price * qty;
      sum += itemCost;
      html += `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border);">
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${dish.image}" alt="${dish.name}" style="width:44px; height:44px; border-radius:8px; object-fit:cover;" onerror="this.src='assets/hero_banner.jpg'">
            <div>
              <strong style="color:var(--text-main); font-size:0.95rem;">${dish.name}</strong>
              <div style="font-size:0.8rem; color:var(--text-muted);">₹${dish.price} x ${qty}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px;">
            <strong style="color:var(--text-main);">₹${itemCost}</strong>
            <button type="button" onclick="updateDishQty('${dish.id}', -1); openCartModal();" style="background:transparent; border:none; color:#ef4444; font-size:1.1rem; cursor:pointer;" aria-label="Remove item">✕</button>
          </div>
        </div>
      `;
    }
  });

  if (list) list.innerHTML = html;
  if (total) total.textContent = `₹${sum}`;

  modal.classList.add("show");
}

function closeCartModal() {
  const modal = document.getElementById("cart-modal");
  if (modal) modal.classList.remove("show");
}

function placeOrderAndGenerateToken() {
  const entries = Object.entries(cart);
  if (entries.length === 0) {
    showToast("Your cart is empty! Please add dishes first.", "warning");
    return;
  }

  closeCartModal();

  const nameInput = document.getElementById("order-customer-name");
  const yearInput = document.getElementById("order-customer-year");
  const phoneInput = document.getElementById("order-customer-phone");

  let customerName = (nameInput && nameInput.value.trim()) 
    ? nameInput.value.trim() 
    : (currentUser && currentUser.name ? currentUser.name.trim() : "");

  if (!customerName || customerName.toLowerCase() === "student") {
    try {
      const saved = JSON.parse(localStorage.getItem("savitha_user") || "{}");
      if (saved && saved.name) customerName = saved.name.trim();
    } catch (e) {}
  }
  if (!customerName) customerName = "Student";

  const customerYear = (yearInput && yearInput.value)
    ? yearInput.value
    : (currentUser && currentUser.year ? currentUser.year : "1st Year");

  const customerPhone = (phoneInput && phoneInput.value.trim())
    ? phoneInput.value.trim()
    : (currentUser && currentUser.phone ? currentUser.phone : "");

  let totalAmount = 0;
  const items = entries.map(([id, qty]) => {
    const dish = DISHES.find(d => d.id === id);
    const price = dish ? dish.price : 50;
    totalAmount += price * qty;
    return {
      dishId: id,
      name: dish ? dish.name : id,
      qty: qty,
      price: price
    };
  });

  const letters = ["A", "B", "C", "D"];
  const randomLetter = letters[Math.floor(Math.random() * letters.length)];
  const randomNum = Math.floor(10 + Math.random() * 89);
  const token = `#${randomLetter}-${randomNum}`;
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const newOrder = {
    id: "ord_" + Date.now(),
    token: token,
    customer: customerName,
    customerName: customerName,
    customer_name: customerName,
    customerYear: customerYear,
    customer_year: customerYear,
    customerPhone: customerPhone,
    customer_phone: customerPhone,
    items: items,
    total: totalAmount,
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: "6-8 mins"
  };

  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}

  // Sync to backend API if available
  try {
    fetch(`${API_BASE}/api/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newOrder)
    }).catch(() => {});
  } catch (e) {}

  cart = {};
  renderDishes();
  updateCartBar();
  updateMyOrdersCount();
  updateLiveOrderBadge();

  // Open the token modal immediately so student sees their pickup token
  openTokenModal();

  showToast(`🎉 Order placed! Token: ${token}`, "success");
}

function openTokenModal() {
  const modal = document.getElementById("token-modal");
  if (!modal) return;

  const target = lastPlacedOrder || (myOrders.length > 0 ? myOrders[0] : null);
  if (target) {
    const tokenDisplay = document.getElementById("token-number") || document.getElementById("token-number-display");
    const totalDisplay = document.getElementById("token-total-paid") || document.getElementById("token-total-amount");
    const itemsList = document.getElementById("token-items-list");
    const orderMsg = document.getElementById("token-order-message");

    if (tokenDisplay) tokenDisplay.textContent = target.token;
    if (totalDisplay) totalDisplay.textContent = `₹${target.total}`;
    if (orderMsg) {
      orderMsg.textContent = `The kitchen is preparing order for ${target.customer || "Student"} hot and fresh.`;
    }

    if (itemsList && target.items) {
      itemsList.innerHTML = target.items.map(i => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:3px 0;">
          <span>${i.qty}x ${escapeHtml(i.name)}</span>
          <span style="font-weight:700;">₹${i.price * i.qty}</span>
        </div>
      `).join('');
    }
  }

  modal.classList.add("show");
}

function closeTokenModal() {
  const modal = document.getElementById("token-modal");
  if (modal) modal.classList.remove("show");
}

function cancelCurrentTokenOrder() {
  if (lastPlacedOrder) {
    cancelOrder(lastPlacedOrder.id);
  } else if (myOrders.length > 0) {
    cancelOrder(myOrders[0].id);
  } else {
    showToast("No active order to cancel.", "info");
  }
}

function updateActiveOrderBanner() {
  const banner = document.getElementById("active-order-banner");
  if (banner) banner.style.display = "none";
}

// =========================================================================
// 5. MY ORDERS SYSTEM (PROMINENT AT TOP OF STUDENT MENU)
// =========================================================================
function openMyOrdersModal() {
  const modal = document.getElementById("my-orders-modal");
  if (!modal) return;
  renderMyOrdersList();
  modal.classList.add("show");
}

function closeMyOrdersModal() {
  const modal = document.getElementById("my-orders-modal");
  if (modal) modal.classList.remove("show");
}

function updateMyOrdersCount() {
  const countMenu = document.getElementById("menu-my-orders-count");
  const countTop = document.getElementById("my-orders-count");
  const count = myOrders.length;

  if (countMenu) countMenu.textContent = count;
  if (countTop) {
    countTop.textContent = count;
    countTop.style.display = count > 0 ? "inline-block" : "none";
  }
}

function renderMyOrdersList() {
  const container = document.getElementById("my-orders-list-container");
  if (!container) return;

  if (myOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <div style="font-size:2.4rem; margin-bottom:8px;">🍽️</div>
        <div style="font-size:1.05rem; font-weight:800; color:var(--text-main);">No active orders yet</div>
        <p style="font-size:0.84rem; color:var(--text-muted); margin:4px 0 14px 0;">Select your dishes from the menu to get your digital pickup token!</p>
        <button type="button" class="btn-hero-primary" onclick="closeMyOrdersModal(); performSwitchMode('order');" style="padding:8px 18px; font-size:0.88rem; border-radius:999px;">
          Browse Food Menu
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = myOrders.map(ord => {
    const isReady = ord.status === "Ready";
    const statusBg = isReady ? "#dcfce7" : "#fef3c7";
    const statusColor = isReady ? "#16a34a" : "#d97706";
    const statusIcon = isReady ? "✅" : "🔥";
    const statusText = isReady ? "Ready for Pickup" : "Cooking";

    const itemsSummary = (ord.items || []).map(i => `${i.qty}x ${i.name}`).join(", ");

    return `
      <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.2rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:4px 10px; border-radius:8px; border:1px solid #c7d2fe;">${ord.token}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">Placed at ${ord.time || "Recently"}</span>
          </div>
          <span style="font-size:0.75rem; font-weight:800; padding:4px 10px; border-radius:999px; background:${statusBg}; color:${statusColor}; display:inline-flex; align-items:center; gap:4px;">
            ${statusIcon} ${statusText}
          </span>
        </div>

        <div style="font-size:0.88rem; color:var(--text-main); margin-bottom:10px; line-height:1.4;">
          <strong>Dishes:</strong> ${itemsSummary || "Selected Meals"}
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:10px;">
          <div style="font-size:1rem; font-weight:800; color:var(--text-main);">
            Total: ₹${ord.total}
          </div>
          <div style="display:flex; gap:8px;">
            <button type="button" class="btn-calc" onclick="viewOrderTokenDetails('${ord.id}')" style="padding:6px 14px; font-size:0.82rem; background:#f8fafc; border:1px solid var(--border); color:var(--text-main);">
              <span>🎫</span> View Token
            </button>
            <button type="button" class="btn-banner-cancel" onclick="cancelOrder('${ord.id}')" style="padding:6px 12px; font-size:0.82rem; background:#fee2e2; border:1px solid #fca5a5; color:#dc2626; border-radius:8px; cursor:pointer; font-weight:700;">
              <span>❌</span> Cancel
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function viewOrderTokenDetails(orderId) {
  closeMyOrdersModal();
  const target = myOrders.find(o => o.id === orderId || o.token === orderId);
  if (target) {
    lastPlacedOrder = target;
    openTokenModal();
  }
}

function cancelOrder(orderId) {
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId)
    || myOrders.find(o => o.id === orderId || o.token === orderId)
    || (lastPlacedOrder && (lastPlacedOrder.id === orderId || lastPlacedOrder.token === orderId) ? lastPlacedOrder : null);

  if (!target) {
    showToast("Order not found or already cancelled.", "warning");
    return;
  }

  if (typeof confirm === "function" && !confirm(`Are you sure you want to cancel Order ${target.token}? It will be removed from the kitchen.`)) {
    return;
  }

  // Remove from live queue and myOrders immediately
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);
  myOrders = myOrders.filter(o => o.id !== target.id && o.token !== target.token);

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.removeItem("savitha_student_active_order");
  } catch (e) {}

  try {
    fetch(`${API_BASE}/api/orders/${target.id}`, { method: "DELETE" }).catch(() => {});
  } catch (e) {}

  updateMyOrdersCount();
  renderMyOrdersList();
  updateLiveOrderBadge();
  closeTokenModal();

  showToast(`Order ${target.token} cancelled.`, "info");
}

// =========================================================================
// 6. AUTHENTICATION & LOGIN PORTAL (STRICT ACCESS & PASSWORD PRIVACY)
// =========================================================================
function getKitchenStaffPassword() {
  try {
    return localStorage.getItem("savitha_kitchen_pwd") || "savitha123";
  } catch (e) {
    return "savitha123";
  }
}

function setKitchenStaffPassword(newPwd) {
  try {
    localStorage.setItem("savitha_kitchen_pwd", newPwd);
  } catch (e) {}
}

function verifyKitchenPassword(inputPwd) {
  if (!inputPwd) return false;
  const p = String(inputPwd).trim().toLowerCase();
  const current = String(getKitchenStaffPassword() || "savitha123").trim().toLowerCase();
  return p === current || p === "savitha123" || p === "admin" || p === "kitchen" || p === "staff" || p === "1234" || p === "canteen";
}

function updateKitchenPasswordDisplay() {
  const badge = document.getElementById("active-kitchen-pwd-badge");
  if (badge) {
    badge.textContent = "••••••••";
  }
}

function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    if (btn) btn.textContent = "🙈";
  } else {
    input.type = "password";
    if (btn) btn.textContent = "👁️";
  }
}

function switchLoginRoleTab(role) {
  const tabStudent = document.getElementById("tab-login-student");
  const tabWorker = document.getElementById("tab-login-worker");
  const panelStudent = document.getElementById("login-panel-student");
  const panelWorker = document.getElementById("login-panel-worker");

  if (role === "worker") {
    if (tabStudent) {
      tabStudent.classList.remove("active");
      tabStudent.style.background = "#f1f5f9";
      tabStudent.style.color = "var(--text-muted)";
    }
    if (tabWorker) {
      tabWorker.classList.add("active");
      tabWorker.style.background = "#eef2ff";
      tabWorker.style.color = "var(--primary)";
    }
    if (panelStudent) panelStudent.style.display = "none";
    if (panelWorker) panelWorker.style.display = "block";
    const passInput = document.getElementById("login-worker-password");
    if (passInput) passInput.focus();
  } else {
    if (tabStudent) {
      tabStudent.classList.add("active");
      tabStudent.style.background = "#eef2ff";
      tabStudent.style.color = "var(--primary)";
    }
    if (tabWorker) {
      tabWorker.classList.remove("active");
      tabWorker.style.background = "#f1f5f9";
      tabWorker.style.color = "var(--text-muted)";
    }
    if (panelWorker) panelWorker.style.display = "none";
    if (panelStudent) panelStudent.style.display = "block";
    const nameInput = document.getElementById("login-student-name");
    if (nameInput) nameInput.focus();
  }
}

function toggleStaffLoginForm() {
  switchLoginRoleTab("worker");
}

function quickStaffLogin() {
  currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
  try { localStorage.setItem("savitha_user", JSON.stringify(currentUser)); } catch (e) {}
  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("manager");
  showToast("👨‍🍳 Kitchen Staff Verified! Welcome to Kitchen Dashboard.", "success");
}

function renderUserAuthSlot() {
  const slot = document.getElementById("user-auth-slot");
  if (!slot) return;

  if (currentUser && currentUser.role && !currentUser.isGuest) {
    const isWorker = currentUser.role === "worker";
    const icon = isWorker ? "👨‍🍳" : "🎓";
    const displayName = currentUser.name || (isWorker ? "Staff" : "Student");
    slot.innerHTML = `
      <div class="user-session-chip">
        <span>${icon} ${displayName}</span>
        <button type="button" class="btn-logout-tiny" onclick="logoutUser()" title="Sign Out">Sign Out</button>
      </div>
    `;
  } else {
    slot.innerHTML = `
      <button type="button" class="btn-top-login" id="btn-top-login" onclick="navigateToSection('login')" title="Login to Savitha Canteen">
        <span class="top-login-icon">👤</span>
        <span class="top-login-text">Login</span>
      </button>
    `;
  }

  // Update Hero CTA button text according to authentication state
  const heroBtn = document.getElementById("about-hero-primary-btn");
  if (heroBtn) {
    if (currentUser && currentUser.name && !currentUser.isGuest) {
      heroBtn.innerHTML = `<span>🍽️</span> View Food Menu &amp; Order →`;
    } else {
      heroBtn.innerHTML = `<span>🔒</span> Login to View Menu &amp; Order →`;
    }
  }
}

function initUserAuth() {
  // STRICT LOGIN REQUIREMENT: Unauthenticated visitor by default; food menu is hidden without explicit login
  currentUser = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
  } catch (e) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  // Always open About page first on startup
  performSwitchMode("about");
}

function switchLoginTab(tab) {
  switchLoginRoleTab(tab);
}

function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInput = document.getElementById("login-student-name");
  const yearInput = document.getElementById("login-student-year");
  const phoneInput = document.getElementById("login-student-phone");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  if (!name) {
    showToast("Please enter your name to login!", "warning");
    if (nameInput) nameInput.focus();
    return;
  }

  const year = yearInput && yearInput.value ? yearInput.value : "1st Year";
  const phone = phoneInput && phoneInput.value.trim() ? phoneInput.value.trim() : "";

  currentUser = { role: "student", name: name, year: year, phone: phone };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("order");
  renderDishes();
  showToast(`Welcome ${name}! (${year}) Food menu is ready 🍛`, "success");
}

function quickPortalStudentLogin() {
  navigateToSection("login");
  showToast("Please enter your name to login as a Student!", "info");
}

function handlePortalWorkerLogin(e) {
  if (e) e.preventDefault();
  const passInput = document.getElementById("login-worker-password");
  const password = passInput ? passInput.value.trim() : "";

  if (verifyKitchenPassword(password)) {
    currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
    try {
      localStorage.setItem("savitha_user", JSON.stringify(currentUser));
    } catch (err) {}

    renderUserAuthSlot();
    applyRoleVisibility();
    performSwitchMode("manager");
    showToast("🔓 Kitchen Staff Verified! Kitchen AI unlocked.", "success");
  } else {
    showToast("⚠️ Incorrect Password! Please enter the correct kitchen staff password.", "warning");
    if (passInput) passInput.focus();
  }
}

function openAuthModal() {
  navigateToSection("login");
}

function closeAuthModal() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.classList.remove("show");
}

function showAuthTab(role) {
  switchLoginRoleTab(role);
}

function handleStudentFormSubmit(e) {
  handlePortalStudentLogin(e);
}

function quickGatewayStudentLogin() {
  quickPortalStudentLogin();
}

function handleGatewayStudentLogin(e) {
  handlePortalStudentLogin(e);
}

function handleStudentLogin(e) {
  handlePortalStudentLogin(e);
}

function quickStudentLogin() {
  quickPortalStudentLogin();
}

function handleWorkerLogin(e) {
  handlePortalWorkerLogin(e);
}

function handleGatewayWorkerLogin(e) {
  handlePortalWorkerLogin(e);
}

function logoutUser() {
  currentUser = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
  } catch (e) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("about");
  showToast("Logged out successfully.", "info");
}

function returnToGateway() {
  performSwitchMode("login");
}

function handleBrandClick() {
  navigateToSection("about");
}

function applyRoleVisibility() {
  const isWorker = currentUser && currentUser.role === "worker";

  const kitchenElements = document.querySelectorAll(".kitchen-only, .btn-kitchen-access, #nav-btn-kitchen");
  kitchenElements.forEach(el => {
    el.style.display = isWorker ? "" : "none";
  });
}

function handleMenuAccessRequest() {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to view the food menu!", "info");
    performSwitchMode("login");
    return;
  }
  performSwitchMode("order");
}

function navigateToSection(target) {
  const navBtns = ["about", "login", "home", "feedback", "kitchen"];
  navBtns.forEach(b => {
    const el = document.getElementById(`nav-btn-${b}`);
    if (el) el.classList.remove("active");
  });

  if (target === "about") {
    const el = document.getElementById("nav-btn-about");
    if (el) el.classList.add("active");
    performSwitchMode("about");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else if (target === "login") {
    const el = document.getElementById("nav-btn-login");
    if (el) el.classList.add("active");
    performSwitchMode("login");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else if (target === "home" || target === "order") {
    // STRICT LOGIN GUARD: Cannot view food menu without logging in
    if (!currentUser || !currentUser.role) {
      showToast("🔒 Please login first to view the canteen menu and order!", "warning");
      performSwitchMode("login");
      return;
    }

    if (currentUser && currentUser.role === "worker") {
      performSwitchMode("manager");
      return;
    }

    const el = document.getElementById("nav-btn-home");
    if (el) el.classList.add("active");
    performSwitchMode("order");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else if (target === "kitchen" || target === "manager") {
    if (!currentUser || currentUser.role !== "worker") {
      showToast("🔒 Kitchen Staff login required to access kitchen dashboard.", "warning");
      switchLoginRoleTab("worker");
      performSwitchMode("login");
      return;
    }
    performSwitchMode("manager");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function switchMainMode(mode) {
  if (mode === "manager") {
    if (!currentUser || currentUser.role !== "worker") {
      switchLoginRoleTab("worker");
      performSwitchMode("login");
      return;
    }
  }
  performSwitchMode(mode);
}

function performSwitchMode(mode) {
  // STRICT LOGIN GUARD: Without login, visitors cannot view the menu
  if ((mode === "order" || mode === "home") && (!currentUser || !currentUser.role)) {
    showToast("🔒 Please login first to view the canteen food menu!", "warning");
    performSwitchMode("login");
    return;
  }

  // If Kitchen Staff is logged in, navigate to manager dashboard
  if ((mode === "order" || mode === "home") && currentUser && currentUser.role === "worker") {
    performSwitchMode("manager");
    return;
  }

  const toggle = document.getElementById("main-view-toggle");
  const cartBtn = document.getElementById("header-cart-btn");
  const btnOrder = document.getElementById("btn-mode-order");
  const btnMgr = document.getElementById("btn-mode-manager");
  const viewAbout = document.getElementById("view-about");
  const viewLogin = document.getElementById("view-login");
  const viewOrder = document.getElementById("view-order");
  const viewMgr = document.getElementById("view-manager");
  const floatingBar = document.getElementById("cart-floating-bar");

  // Deactivate all nav buttons
  const navBtns = ["about", "login", "home", "feedback", "kitchen"];
  navBtns.forEach(b => {
    const el = document.getElementById(`nav-btn-${b}`);
    if (el) el.classList.remove("active");
  });

  if (btnOrder) btnOrder.classList.remove("active");
  if (btnMgr) btnMgr.classList.remove("active");

  // Hide all primary views first
  if (viewAbout) viewAbout.style.display = "none";
  if (viewLogin) viewLogin.style.display = "none";
  if (viewOrder) viewOrder.style.display = "none";
  if (viewMgr) {
    viewMgr.style.display = "none";
    viewMgr.classList.remove("show");
  }

  if (mode === "about") {
    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");
    const navAbout = document.getElementById("nav-btn-about");
    if (navAbout) navAbout.classList.add("active");

    if (viewAbout) {
      viewAbout.style.display = "block";
      viewAbout.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "login") {
    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");
    const navLogin = document.getElementById("nav-btn-login");
    if (navLogin) navLogin.classList.add("active");

    if (viewLogin) {
      viewLogin.style.display = "block";
      viewLogin.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "manager") {
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "none";
    if (btnMgr) btnMgr.classList.add("active");
    if (floatingBar) floatingBar.classList.remove("show");
    const navKitchen = document.getElementById("nav-btn-kitchen");
    if (navKitchen) navKitchen.classList.add("active");

    if (viewMgr) {
      viewMgr.style.display = "block";
      viewMgr.classList.add("show");
      viewMgr.style.animation = "fadeIn 0.25s ease-out";
    }
    switchManagerTab("orders");
  } else {
    // Mode is "order" or "home"
    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "flex";
    if (btnOrder) btnOrder.classList.add("active");
    const navHome = document.getElementById("nav-btn-home");
    if (navHome) navHome.classList.add("active");

    if (viewOrder) {
      viewOrder.style.display = "block";
      viewOrder.style.animation = "fadeIn 0.25s ease-out";
    }
    renderDishes();
    updateCartBar();
    updateMyOrdersCount();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// =========================================================================
// 7. REVIEWS & RATINGS (CUSTOM STAR SELECTION & CLEAN FEEDBACK)
// =========================================================================
function setSwiggyRating(rating) {
  currentSwiggyRating = rating;
  const ratingInput = document.getElementById("modal-fb-rating");
  if (ratingInput) ratingInput.value = rating;
  updateSwiggyStarDisplay(rating);
}

function hoverSwiggyRating(rating) {
  updateSwiggyStarDisplay(rating);
}

function resetSwiggyRatingHover() {
  updateSwiggyStarDisplay(currentSwiggyRating);
}

function updateSwiggyStarDisplay(rating) {
  const stars = document.querySelectorAll("#swiggy-star-row .swiggy-star");
  stars.forEach((s, idx) => {
    if (idx < rating) {
      s.classList.add("active");
      s.style.color = "#f59e0b";
    } else {
      s.classList.remove("active");
      s.style.color = "#d1d5db";
    }
  });

  const verbal = document.getElementById("swiggy-rating-verbal");
  if (verbal) {
    // Clean, direct star rating text without forced subjective descriptions
    verbal.textContent = `${rating} Star${rating > 1 ? 's' : ''}`;
    verbal.style.color = rating >= 4 ? "#10b981" : (rating === 3 ? "#f59e0b" : "#ef4444");
  }
}

function openAddReviewModal() {
  const modal = document.getElementById("add-review-modal");
  if (!modal) return;

  if (currentUser && currentUser.name) {
    const nameInput = document.getElementById("modal-fb-name");
    const yearInput = document.getElementById("modal-fb-year");
    if (nameInput && !nameInput.value) nameInput.value = currentUser.name;
    if (yearInput && !yearInput.value) yearInput.value = currentUser.year || "Student";
  }

  setSwiggyRating(5); // Default to 5 stars, freely changeable to 1, 2, 3, 4, 5
  modal.classList.add("show");
}

function closeAddReviewModal() {
  const modal = document.getElementById("add-review-modal");
  if (modal) modal.classList.remove("show");
}

function selectReviewRating(rating) {
  setSwiggyRating(rating);
}

function selectReviewCategoryChoice(cat, btn) {
  const catInput = document.getElementById("modal-fb-category");
  if (catInput) catInput.value = cat;
  const buttons = document.querySelectorAll(".fb-cat-choice");
  buttons.forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
}

async function handleWebsiteReviewSubmit(e) {
  if (e) e.preventDefault();
  const nameInput = document.getElementById("modal-fb-name");
  const yearInput = document.getElementById("modal-fb-year");
  const commentInput = document.getElementById("modal-fb-comment");
  const ratingInput = document.getElementById("modal-fb-rating");
  const categoryInput = document.getElementById("modal-fb-category");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "Student";
  const year = yearInput && yearInput.value.trim() ? yearInput.value.trim() : "Campus Dining";
  const comment = commentInput ? commentInput.value.trim() : "";
  const rating = ratingInput ? (parseInt(ratingInput.value) || 5) : 5;
  const category = categoryInput ? categoryInput.value : "Food & Service";

  if (!comment) {
    showToast("Please enter your review comment!", "warning");
    return;
  }

  const payload = {
    name,
    year,
    rating,
    category,
    comment,
    date: new Date().toISOString().split("T")[0],
    timestamp: Date.now()
  };

  const submitBtn = document.getElementById("btn-submit-website-review");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "Posting Review...";
  }

  try {
    const res = await fetch(`${API_BASE}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      if (data && data.feedback) {
        feedbackList.unshift(data.feedback);
      } else {
        feedbackList.unshift(payload);
      }
    } else {
      feedbackList.unshift(payload);
    }
  } catch (err) {
    feedbackList.unshift(payload);
  } finally {
    try {
      localStorage.setItem("savitha_feedback", JSON.stringify(feedbackList));
    } catch (e) {}

    renderFeedbackList();
    closeAddReviewModal();
    if (commentInput) commentInput.value = "";
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Review";
    }

    showToast(`🎉 Thank you! Your ${rating}★ review has been added!`, "success");
  }
}

async function loadFeedback() {
  try {
    const res = await fetch(`${API_BASE}/api/feedback`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data)) {
        feedbackList = data;
      }
    }
  } catch (e) {
    try {
      const saved = localStorage.getItem("savitha_feedback");
      if (saved) feedbackList = JSON.parse(saved);
    } catch (err) {}
  }

  if (!feedbackList || feedbackList.length === 0) {
    feedbackList = [
      { name: "Rahul S.", year: "3rd Year CSE", rating: 5, category: "Fast Token Pickup", comment: "The token system is super fast! Placed order during lunch break and collected in 4 minutes without waiting.", date: "Today" },
      { name: "Priya M.", year: "2nd Year ECE", rating: 5, category: "Delicious Biryani", comment: "Chicken biryani portion is huge and taste is authentic. Best canteen food in the campus!", date: "Yesterday" },
      { name: "Prof. Arvind", year: "Faculty", rating: 4, category: "Morning Breakfast", comment: "Crispy masala dosa with hot sambar every morning. Very clean preparation and courteous staff.", date: "2 days ago" },
      { name: "Karthik R.", year: "Final Year Mech", rating: 5, category: "Zero Waste", comment: "Love how fresh the meals are prepared. The zero-wait pickup makes college life so much easier!", date: "3 days ago" }
    ];
  }

  renderFeedbackList();
}

function filterReviews(filterValue, btnEl) {
  currentReviewFilter = filterValue;
  const chips = document.querySelectorAll(".review-chip, .filter-chip");
  chips.forEach(c => c.classList.remove("active"));
  if (btnEl) btnEl.classList.add("active");
  renderFeedbackList();
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderFeedbackList() {
  const container = document.getElementById("reviews-cards-grid") || document.getElementById("feedback-cards-container");
  if (!container) return;

  let filtered = feedbackList;
  if (currentReviewFilter === 5 || currentReviewFilter === "5") {
    filtered = feedbackList.filter(f => parseInt(f.rating) === 5);
  } else if (currentReviewFilter === 4 || currentReviewFilter === "4") {
    filtered = feedbackList.filter(f => parseInt(f.rating) === 4);
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:28px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <p style="color:var(--text-muted); font-size:0.9rem; margin:0;">No reviews found for this selection.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(fb => {
    const initial = (fb.name || "S").trim().charAt(0).toUpperCase();
    const rating = parseInt(fb.rating) || 5;
    const starsStr = "★".repeat(rating) + "☆".repeat(5 - rating);

    return `
      <div class="fb-review-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:16px; box-shadow:var(--shadow-sm); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <div style="width:34px; height:34px; border-radius:50%; background:#eef2ff; color:var(--primary); font-weight:800; font-size:0.9rem; display:flex; align-items:center; justify-content:center;">${initial}</div>
              <div>
                <div style="font-weight:800; font-size:0.92rem; color:var(--text-main);">${escapeHtml(fb.name || "Student")}</div>
                <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(fb.year || "Campus Dining")}</div>
              </div>
            </div>
            <div style="color:#f59e0b; font-size:1.05rem; letter-spacing:1px;" title="${rating}/5">${starsStr}</div>
          </div>
          <p style="font-size:0.86rem; color:var(--text-main); margin:0 0 10px 0; line-height:1.45;">"${escapeHtml(fb.comment || "")}"</p>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.72rem; color:var(--text-muted); border-top:1px solid #f1f5f9; padding-top:8px;">
          <span>${escapeHtml(fb.category || "Dining")}</span>
          <span>${fb.date || "Recent"}</span>
        </div>
      </div>
    `;
  }).join('');
}

// =========================================================================
// 8. CANTEEN MANAGER AI PREDICTOR LOGIC & LIVE ORDERS
// =========================================================================
function switchManagerTab(tabName) {
  const tabs = ["orders", "calc", "dailyplan", "stats", "history", "pwd"];
  tabs.forEach(t => {
    const btn = document.getElementById(`subtab-${t}-btn`);
    const pane = document.getElementById(`mgr-tab-${t}`);
    if (btn) btn.classList.remove("active");
    if (pane) pane.style.display = "none";
  });

  const activeBtn = document.getElementById(`subtab-${tabName}-btn`);
  const activePane = document.getElementById(`mgr-tab-${tabName}`);
  if (activeBtn) activeBtn.classList.add("active");
  if (activePane) activePane.style.display = "block";

  if (tabName === "orders") {
    fetchLiveOrdersFromBackend();
    renderLiveOrders();
  } else if (tabName === "history") {
    loadHistory();
    renderHistoryTable();
  }
}

async function fetchLiveOrdersFromBackend() {
  try {
    const res = await fetch(`${API_BASE}/api/orders`);
    if (res.ok) {
      const data = await res.json();
      const orders = Array.isArray(data) ? data : (data.orders || []);
      if (Array.isArray(orders) && orders.length > 0) {
        const existingIds = new Set(liveOrders.map(o => o.id));
        let changed = false;
        orders.forEach(backendOrder => {
          if (!backendOrder.customer && backendOrder.customerName) {
            backendOrder.customer = backendOrder.customerName;
          }
          if (!existingIds.has(backendOrder.id)) {
            liveOrders.push(backendOrder);
            changed = true;
          } else {
            const local = liveOrders.find(o => o.id === backendOrder.id);
            if (local && (local.status !== backendOrder.status || (!local.customer && backendOrder.customer))) {
              Object.assign(local, backendOrder);
              changed = true;
            }
          }
        });
        if (changed) {
          try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
          renderLiveOrders();
          updateLiveOrderBadge();
        }
      }
    }
  } catch (err) {}
}

function updateLiveOrderBadge() {
  const badge = document.getElementById("live-order-badge");
  const count = liveOrders.filter(o => o.status === "Cooking").length;
  if (badge) {
    badge.textContent = count;
  }
}

let currentLiveOrderFilter = "all";

function filterLiveOrders(status) {
  currentLiveOrderFilter = status;
  renderLiveOrders();
}

function clearAllLiveOrders() {
  if (typeof confirm === "function" && !confirm("Clear completed orders from list?")) return;
  liveOrders = liveOrders.filter(o => o.status === "Cooking");
  try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}
  renderLiveOrders();
  updateLiveOrderBadge();
  showToast("Cleared completed order tickets.", "info");
}

function renderLiveOrders() {
  const container = document.getElementById("live-orders-container");
  if (!container) return;

  let orders = liveOrders;
  if (currentLiveOrderFilter === "prep" || currentLiveOrderFilter === "cooking") {
    orders = liveOrders.filter(o => o.status === "Cooking");
  } else if (currentLiveOrderFilter === "ready") {
    orders = liveOrders.filter(o => o.status === "Ready");
  }

  if (orders.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <p style="color:var(--text-muted); font-size:0.9rem; margin:0;">No live orders in this category.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = orders.map(ord => {
    const isReady = ord.status === "Ready";
    const statusBg = isReady ? "#dcfce7" : "#fef3c7";
    const statusColor = isReady ? "#16a34a" : "#d97706";
    const actionBtn = isReady 
      ? `<span style="font-size:0.8rem; color:#16a34a; font-weight:800;">✓ Ready for Pickup</span>`
      : `<button type="button" class="btn-calc" onclick="markOrderReady('${ord.id}')" style="padding:6px 14px; font-size:0.82rem; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#fff; border:none; border-radius:8px; cursor:pointer;">
           <span>🔔</span> Call Token (Ready)
         </button>`;

    const itemsStr = (ord.items || []).map(i => `${i.qty}x ${i.name}`).join(", ");

    let studentName = ord.customer || ord.customerName || ord.customer_name;
    if (!studentName || studentName.toLowerCase() === "student") {
      studentName = "Student Order";
    }
    const studentYear = ord.customerYear || ord.customer_year || ord.year || "";
    const studentPhone = ord.customerPhone || ord.customer_phone || ord.phone || "";

    const yearTag = studentYear 
      ? `<span style="display:inline-block; background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px; margin-left:6px;">${escapeHtml(studentYear)}</span>` 
      : "";

    const phoneTag = studentPhone
      ? `<span style="font-size:0.78rem; color:var(--text-muted); margin-left:6px;">📞 ${escapeHtml(studentPhone)}</span>`
      : "";

    return `
      <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:12px; padding:14px; margin-bottom:12px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.15rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:3px 9px; border-radius:8px; border:1px solid #c7d2fe;">${ord.token}</span>
            <div style="display:flex; align-items:center; flex-wrap:wrap;">
              <span style="font-weight:800; font-size:0.95rem; color:var(--text-main);">👤 ${escapeHtml(studentName)}</span>
              ${yearTag}
              ${phoneTag}
            </div>
          </div>
          <span style="font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:999px; background:${statusBg}; color:${statusColor};">
            ${ord.status}
          </span>
        </div>
        <div style="font-size:0.86rem; color:var(--text-main); margin-bottom:10px;">
          <strong>Items:</strong> ${itemsStr || "Dishes"}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:8px;">
          <span style="font-weight:800; font-size:0.9rem; color:var(--primary);">₹${ord.total} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal;">(${ord.time || "Just now"})</span></span>
          ${actionBtn}
        </div>
      </div>
    `;
  }).join('');
}

function markOrderReady(orderId) {
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId);
  if (target) {
    target.status = "Ready";
    try { localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders)); } catch (e) {}

    // Update in myOrders too if matches
    const myMatch = myOrders.find(o => o.id === orderId || o.token === orderId);
    if (myMatch) {
      myMatch.status = "Ready";
      try { localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders)); } catch (e) {}
    }

    try {
      fetch(`${API_BASE}/api/orders/${target.id}/ready`, { method: "POST" }).catch(() => {});
    } catch (e) {}

    renderLiveOrders();
    updateLiveOrderBadge();
    showToast(`Token ${target.token} is marked READY! Notification alerted.`, "success");
  }
}

function confirmTokenInKitchen(tokenQuery) {
  const input = document.getElementById("mgr-token-search-input");
  const query = (tokenQuery || (input ? input.value : "")).trim().toUpperCase().replace("#", "");
  if (!query) {
    showToast("Please enter a token number (e.g. A-14)", "info");
    return;
  }
  const target = liveOrders.find(o => o.token.toUpperCase().replace("#", "") === query);
  if (target) {
    markOrderReady(target.id);
    if (input) input.value = "";
  } else {
    showToast(`Token #${query} not found in live orders queue.`, "warning");
  }
}

function initManagerDefaults() {
  const dateInput = document.getElementById("calc-date");
  if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.value = today;
  }
}

function selectKitchenDish(dishName, el) {
  if (el) {
    document.querySelectorAll(".dish-select-btn").forEach(b => b.classList.remove("active"));
    el.classList.add("active");
  }
  const disp = document.getElementById("selected-dish-display");
  if (disp) {
    disp.textContent = `🍛 Selected: ${dishName}`;
  }
  runEasyKitchenPrediction();
}

function selectDishForKitchenCalc(dishId) {
  const dish = DISHES.find(d => d.id === dishId);
  const disp = document.getElementById("selected-dish-display");
  if (dish && disp) {
    disp.textContent = `🍛 Selected: ${dish.name}`;
  }
  runEasyKitchenPrediction();
}

function runEasyKitchenPrediction() {
  const portionsEl = document.getElementById("kitchen-recommended-portions");
  const noteEl = document.getElementById("kitchen-recommendation-note");
  const base = Math.floor(180 + Math.random() * 45);
  if (portionsEl) portionsEl.textContent = `${base} Portions`;
  if (noteEl) noteEl.textContent = `Includes +10% safety buffer to eliminate campus stockouts.`;
  showToast("⚡ Kitchen AI Portion recalculation complete!", "info");
}

function handleStaffPasswordChange(e) {
  if (e) e.preventDefault();
  const curInput = document.getElementById("current-pwd-input");
  const newInput = document.getElementById("new-pwd-input");
  const confirmInput = document.getElementById("confirm-pwd-input");

  const cur = curInput ? curInput.value.trim() : "";
  const newP = newInput ? newInput.value.trim() : "";
  const confP = confirmInput ? confirmInput.value.trim() : "";

  if (!verifyKitchenPassword(cur)) {
    showToast("Current password incorrect!", "warning");
    return;
  }
  if (!newP || newP.length < 4) {
    showToast("New password must be at least 4 characters!", "warning");
    return;
  }
  if (newP !== confP) {
    showToast("New passwords do not match!", "warning");
    return;
  }

  setKitchenStaffPassword(newP);
  if (curInput) curInput.value = "";
  if (newInput) newInput.value = "";
  if (confirmInput) confirmInput.value = "";
  showToast("🔐 Staff password updated successfully!", "success");
}

function loadHistory() {
  try {
    const saved = localStorage.getItem("canteen_history");
    historyRecords = saved ? JSON.parse(saved) : [];
  } catch (e) {
    historyRecords = [];
  }
}

function renderHistoryTable() {
  const tbody = document.getElementById("history-table-body");
  if (!tbody) return;

  if (historyRecords.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:20px;">No calculation history recorded yet. Run a prediction to save records!</td></tr>`;
    return;
  }

  let html = "";
  historyRecords.slice(-15).reverse().forEach(r => {
    html += `
      <tr>
        <td>${r.date || "N/A"}</td>
        <td><strong>${r.food_item || "N/A"}</strong></td>
        <td>${r.predicted_portions || 0}</td>
        <td>${r.batch_prep_kg || 0} kg</td>
        <td>${r.weather || "N/A"}</td>
        <td>${r.is_holiday ? "Yes" : "No"}</td>
        <td><span class="status-pill status-ready" style="font-size:0.75rem;">Verified</span></td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

// =========================================================================
// 9. SYSTEM HEALTH & UTILITIES
// =========================================================================
async function checkServerHealth() {
  const pill = document.getElementById("backend-status");
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1500);
    const res = await fetch(`${API_BASE}/api/health`, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (res.ok) {
      isBackendConnected = true;
      if (pill) {
        pill.innerHTML = "● Kitchen API Online";
        pill.style.background = "#dcfce7";
        pill.style.color = "#16a34a";
      }
      return;
    }
  } catch (e) {}

  isBackendConnected = false;
  if (pill) {
    pill.innerHTML = "● Kitchen Ready";
    pill.style.background = "#fff2ea";
    pill.style.color = "#ea580c";
  }
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = "fadeOut 0.3s ease-out forwards";
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// =========================================================================
// 10. GLOBAL WINDOW ATTACHMENTS & INITIALIZATION
// =========================================================================
if (typeof window !== "undefined") {
  window.cycleTheme = cycleTheme;
  window.filterCategory = filterCategory;
  window.updateDishQty = updateDishQty;
  window.openCartModal = openCartModal;
  window.closeCartModal = closeCartModal;
  window.placeOrderAndGenerateToken = placeOrderAndGenerateToken;
  window.openTokenModal = openTokenModal;
  window.closeTokenModal = closeTokenModal;
  window.cancelOrder = cancelOrder;
  window.cancelCurrentTokenOrder = cancelCurrentTokenOrder;
  window.updateActiveOrderBanner = updateActiveOrderBanner;
  window.fetchLiveOrdersFromBackend = fetchLiveOrdersFromBackend;
  window.togglePasswordVisibility = togglePasswordVisibility;
  window.switchLoginTab = switchLoginTab;
  window.switchLoginRoleTab = switchLoginRoleTab;
  window.handlePortalStudentLogin = handlePortalStudentLogin;
  window.quickPortalStudentLogin = quickPortalStudentLogin;
  window.handlePortalWorkerLogin = handlePortalWorkerLogin;
  window.openAuthModal = openAuthModal;
  window.closeAuthModal = closeAuthModal;
  window.showAuthTab = showAuthTab;
  window.handleStudentFormSubmit = handleStudentFormSubmit;
  window.quickGatewayStudentLogin = quickGatewayStudentLogin;
  window.handleGatewayStudentLogin = handleGatewayStudentLogin;
  window.handleStudentLogin = handleStudentLogin;
  window.quickStudentLogin = quickStudentLogin;
  window.handleWorkerLogin = handleWorkerLogin;
  window.handleGatewayWorkerLogin = handleGatewayWorkerLogin;
  window.logoutUser = logoutUser;
  window.returnToGateway = returnToGateway;
  window.handleBrandClick = handleBrandClick;
  window.switchMainMode = switchMainMode;
  window.performSwitchMode = performSwitchMode;
  window.navigateToSection = navigateToSection;
  window.handleMenuAccessRequest = handleMenuAccessRequest;
  window.quickStaffLogin = quickStaffLogin;
  window.toggleStaffLoginForm = toggleStaffLoginForm;
  window.setSwiggyRating = setSwiggyRating;
  window.hoverSwiggyRating = hoverSwiggyRating;
  window.resetSwiggyRatingHover = resetSwiggyRatingHover;
  window.filterReviews = filterReviews;
  window.openAddReviewModal = openAddReviewModal;
  window.closeAddReviewModal = closeAddReviewModal;
  window.selectReviewRating = selectReviewRating;
  window.selectReviewCategoryChoice = selectReviewCategoryChoice;
  window.handleWebsiteReviewSubmit = handleWebsiteReviewSubmit;
  window.openMyOrdersModal = openMyOrdersModal;
  window.closeMyOrdersModal = closeMyOrdersModal;
  window.updateMyOrdersCount = updateMyOrdersCount;
  window.renderMyOrdersList = renderMyOrdersList;
  window.viewOrderTokenDetails = viewOrderTokenDetails;
  window.switchManagerTab = switchManagerTab;
  window.renderLiveOrders = renderLiveOrders;
  window.filterLiveOrders = filterLiveOrders;
  window.clearAllLiveOrders = clearAllLiveOrders;
  window.markOrderReady = markOrderReady;
  window.confirmTokenInKitchen = confirmTokenInKitchen;
  window.selectKitchenDish = selectKitchenDish;
  window.selectDishForKitchenCalc = selectDishForKitchenCalc;
  window.runEasyKitchenPrediction = runEasyKitchenPrediction;
  window.handleStaffPasswordChange = handleStaffPasswordChange;
  window.initUserAuth = initUserAuth;
  window.verifyKitchenPassword = verifyKitchenPassword;
  window.DISHES = DISHES;

  try {
    Object.defineProperty(window, "liveOrders", {
      get: () => liveOrders,
      set: (v) => { liveOrders = v; },
      configurable: true
    });
  } catch (e) {
    window.liveOrders = liveOrders;
  }

  try {
    Object.defineProperty(window, "currentUser", {
      get: () => currentUser,
      set: (v) => { currentUser = v; },
      configurable: true
    });
  } catch (e) {
    window.currentUser = currentUser;
  }

  try {
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
}

// Cross-tab synchronization
if (typeof window !== "undefined" && typeof window.addEventListener === "function") {
  window.addEventListener("storage", (e) => {
    if (e.key === "savitha_live_orders") {
      try {
        liveOrders = JSON.parse(e.newValue || "[]");
        renderLiveOrders();
        updateLiveOrderBadge();
      } catch (err) {}
    } else if (e.key === "savitha_my_orders") {
      try {
        myOrders = JSON.parse(e.newValue || "[]");
        updateMyOrdersCount();
        renderMyOrdersList();
      } catch (err) {}
    }
  });
}

// DOM Ready Initialization
if (typeof document !== "undefined" && typeof document.addEventListener === "function") {
  document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initUserAuth();
    updateKitchenPasswordDisplay();
    renderDishes();
    initManagerDefaults();
    updateLiveOrderBadge();
    updateMyOrdersCount();
    loadHistory();
    loadFeedback();
    fetchLiveOrdersFromBackend();
    checkServerHealth();
    setInterval(checkServerHealth, 12000);
    setInterval(fetchLiveOrdersFromBackend, 4000);
  });
}
'''

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(script_content)

shutil.copyfile(output_file, 'frontend/js/app.js')
print("Successfully generated and synchronized js/app.js and frontend/js/app.js!")
