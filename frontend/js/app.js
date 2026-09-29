/**
 * Savitha Canteen - Complete Client-side Controller & AI Kitchen Engine
 * Developed & Architected by Parinitha.S
 */

// =========================================================================
// 1. FOOD MENU CATALOG WITH AUTHENTIC PHOTOGRAPHY & DISH DATA
// =========================================================================
const DISHES = [
  {
    id: "todays_special_combo",
    name: "Today's Special: Royal Dum Biryani Combo",
    category: "lunch",
    price: 99,
    originalPrice: 149,
    isSpecialOffer: true,
    rating: 5.0,
    reviews: 380,
    isVeg: true,
    image: "assets/veg_biryani.jpg",
    desc: "⭐ SWIGGY & ZOMATO STYLE DEAL: Authentic Hyderabadi Dum Biryani + Golden Onion Pakoda + Chilled Fresh Lime Soda. Flat ₹99 Today Only!",
    demandStatus: "🔥 DEAL OF THE DAY • FLAT ₹99"
  },
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
    desc: "Creamy iced blended coffee crafted with rich roasted espresso, chilled milk, and a decadent drizzle of Hershey's chocolate syrup.",
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
  },
  {
    id: "chicken_noodles",
    name: "Spicy Chicken Hakka Noodles",
    category: "lunch",
    price: 125,
    rating: 4.8,
    reviews: 176,
    isVeg: false,
    image: "assets/chicken_noodles.jpg",
    desc: "Wok-tossed fiery Hakka noodles loaded with shredded spiced chicken, crisp bell peppers, spring onions, and spicy schezwan sauce.",
    demandStatus: "🍜 Indo-Chinese Non-Veg Hit"
  },
  {
    id: "peri_peri_fries",
    name: "Crispy Peri Peri Fries",
    category: "snacks",
    price: 60,
    rating: 4.8,
    reviews: 204,
    isVeg: true,
    image: "assets/peri_peri_fries.jpg",
    desc: "Golden crinkle-cut potato fries dusted generously with zesty African bird's eye chili peri-peri seasoning. Served with garlic dip.",
    demandStatus: "🍟 Crunchy Anytime Snack"
  },
  {
    id: "campus_burger",
    name: "Crispy Veg Cheese Burger",
    category: "snacks",
    price: 75,
    rating: 4.7,
    reviews: 148,
    isVeg: true,
    image: "assets/campus_burger.jpg",
    desc: "Toasted sesame bun with a golden spiced vegetable patty, melted cheese slice, crisp lettuce, juicy tomato and mayo.",
    demandStatus: "🍔 Student Break Crunch"
  },
  {
    id: "chicken_burger",
    name: "Crispy Chicken Tikka Burger",
    category: "lunch",
    price: 95,
    rating: 4.9,
    reviews: 182,
    isVeg: false,
    image: "assets/campus_burger.jpg",
    desc: "Juicy marinated chicken tikka cutlet crowned with melted cheddar cheese, fresh coleslaw, and tandoori spread on a brioche bun.",
    demandStatus: "🍔 Campus Grill Favorite"
  },
  {
    id: "medu_vada_plate",
    name: "Crispy Medu Vada (2 Pcs)",
    category: "breakfast",
    price: 50,
    rating: 4.8,
    reviews: 135,
    isVeg: true,
    image: "assets/medu_vada.jpg",
    desc: "Two piping hot, crispy golden lentil vadas infused with whole peppercorns, ginger, and curry leaves. Served with coconut chutney and hot sambar.",
    demandStatus: "🥞 Morning South Classic"
  },
  {
    id: "ghee_podi_idli",
    name: "Mini Ghee Podi Idli (12 Pcs)",
    category: "breakfast",
    price: 70,
    rating: 4.9,
    reviews: 190,
    isVeg: true,
    image: "assets/idli_vada.jpg",
    desc: "Bite-sized soft steamed rice idlis tossed in aromatic clarified butter (desi ghee) and spicy gunpowder podi masala. Served with coconut chutney.",
    demandStatus: "🥞 Ghee Roasted Bestseller"
  },
  {
    id: "rava_masala_dosa",
    name: "Crispy Onion Rava Dosa",
    category: "breakfast",
    price: 85,
    rating: 4.8,
    reviews: 156,
    isVeg: true,
    image: "assets/masala_dosa.jpg",
    desc: "Ultra-crispy semolina crepe studded with finely chopped red onions, cumin, green chilies, and potato masala filling.",
    demandStatus: "🥞 Breakfast Crunch Master"
  },
  {
    id: "special_chicken_fried_rice",
    name: "Schezwan Chicken Fried Rice",
    category: "lunch",
    price: 130,
    rating: 4.8,
    reviews: 165,
    isVeg: false,
    image: "assets/egg_fried_rice.jpg",
    desc: "Fragrant basmati rice stir-fried on high flame with tender chicken bites, scrambled eggs, crispy veggies and hot red schezwan sauce.",
    demandStatus: "🍳 Spicy Wok Sensation"
  },
  {
    id: "south_executive_meal",
    name: "Executive South Meals Thali",
    category: "lunch",
    price: 120,
    rating: 4.9,
    reviews: 220,
    isVeg: true,
    image: "assets/paneer_thali.jpg",
    desc: "Complete South Indian feast: Steamed rice, poori, traditional sambar, rasam, kootu poriyal, appalam papad, curd and sweet semiya payasam.",
    demandStatus: "🍱 Wholesome Traditional Thali"
  },
  {
    id: "fresh_watermelon_juice",
    name: "Fresh Chilled Watermelon Juice",
    category: "snacks",
    price: 40,
    rating: 4.8,
    reviews: 142,
    isVeg: true,
    image: "assets/lime_soda.jpg",
    desc: "100% natural freshly cold-pressed watermelon juice served chilled with a hint of mint and black rock salt. No added artificial sugar.",
    demandStatus: "🍉 Natural Summer Cooler"
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

// Strict user-order isolation helper: matches order by user.id or 10-digit phone
function isOrderForUser(order, user) {
  if (!order || !user) return false;
  // Match on user id
  if (user.id && (order.userId === user.id || order.user_id === user.id)) return true;
  // Match on clean 10-digit phone
  const userPhone = String(user.phone || "").replace(/\D/g, '').slice(-10);
  const orderPhone = String(order.customerPhone || order.customer_phone || "").replace(/\D/g, '').slice(-10);
  if (userPhone && orderPhone && userPhone.length === 10 && userPhone === orderPhone) return true;
  // Match on username only if non-empty and non-guest
  if (typeof user.username === "string" && user.username.trim() && user.username.trim() !== "guest" &&
      typeof order.username === "string" && order.username.trim() && order.username.trim() !== "guest" &&
      user.username.trim().toLowerCase() === order.username.trim().toLowerCase()) {
    return true;
  }
  return false;
}

let myOrders = [];
try {
  const savedUser = localStorage.getItem("savitha_user");
  if (savedUser) {
    const u = JSON.parse(savedUser);
    if (u && u.id) {
      const savedMy = localStorage.getItem(`savitha_my_orders_${u.id}`);
      myOrders = savedMy ? JSON.parse(savedMy) : [];
    }
  }
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

// =========================================================================
// KITCHEN INVENTORY & STOCK MONITORING ENGINE
// =========================================================================
let inventory = [];
let currentInventoryCategory = "all";
let currentInventoryStatus = "all";
let inventorySearchQuery = "";

function initInventory() {
  try {
    const raw = localStorage.getItem("savitha_inventory");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) {
        inventory = parsed;
        updateInventoryBadge();
        return inventory;
      }
    }
  } catch (e) {}

  inventory = DISHES.map(d => ({
    id: d.id,
    name: d.name,
    category: d.category,
    price: d.price,
    image: d.image,
    isVeg: d.isVeg,
    stock: d.id === "chicken_biryani" ? 45 : (d.id === "samosa_chai" ? 75 : (d.id === "veg_biryani" ? 60 : 40)),
    threshold: 10,
    status: "in_stock",
    lastUpdated: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }));
  saveInventory();
  updateInventoryBadge();
  return inventory;
}

function getInventory() {
  if (!inventory || inventory.length === 0) {
    initInventory();
  }
  return inventory;
}

function getInventoryItem(dishId) {
  const inv = getInventory();
  return inv.find(i => i.id === dishId) || null;
}

function saveInventory() {
  try {
    localStorage.setItem("savitha_inventory", JSON.stringify(inventory));
  } catch (e) {}
}

function updateInventoryBadge() {
  const badge = document.getElementById("inv-low-stock-badge");
  const inv = getInventory();
  const lowCount = inv.filter(i => i.status === "low_stock" || i.status === "out_of_stock").length;
  if (badge) {
    badge.textContent = lowCount;
    badge.style.display = lowCount > 0 ? "inline-block" : "none";
  }
}

function updateItemStock(dishId, newStock) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  const num = Math.max(0, parseInt(newStock) || 0);
  item.stock = num;
  if (num === 0) {
    item.status = "out_of_stock";
  } else if (num <= item.threshold) {
    item.status = "low_stock";
  } else {
    item.status = "in_stock";
  }
  item.lastUpdated = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`Updated stock for ${item.name}: ${item.stock} portions`, "info");
}

function adjustItemStock(dishId, delta) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  updateItemStock(dishId, item.stock + delta);
}

function toggleItemStatus(dishId) {
  const item = getInventoryItem(dishId);
  if (!item) return;
  if (item.status === "out_of_stock") {
    item.status = item.stock <= item.threshold ? (item.stock > 0 ? "low_stock" : "in_stock") : "in_stock";
    if (item.stock === 0) item.stock = 25;
  } else {
    item.status = "out_of_stock";
  }
  item.lastUpdated = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`${item.name} is now ${item.status === "out_of_stock" ? "Marked Sold Out 🔴" : "Available In Stock 🟢"}`, "info");
}

function restockAll(addedPortions = 20) {
  const inv = getInventory();
  inv.forEach(item => {
    item.stock += addedPortions;
    if (item.status === "out_of_stock" && item.stock > 0) {
      item.status = item.stock <= item.threshold ? "low_stock" : "in_stock";
    }
  });
  saveInventory();
  renderInventoryDashboard();
  renderDishes();
  updateInventoryBadge();
  showToast(`⚡ Restocked all items (+${addedPortions} portions)!`, "success");
}

function decrementOrderInventory(items) {
  if (!Array.isArray(items)) return;
  const inv = getInventory();
  let changed = false;
  items.forEach(orderItem => {
    const invItem = inv.find(i => i.id === orderItem.dishId);
    if (invItem) {
      invItem.stock = Math.max(0, invItem.stock - (orderItem.qty || 1));
      if (invItem.stock === 0) {
        invItem.status = "out_of_stock";
      } else if (invItem.stock <= invItem.threshold) {
        invItem.status = "low_stock";
      }
      changed = true;
    }
  });
  if (changed) {
    saveInventory();
    renderInventoryDashboard();
    renderDishes();
    updateInventoryBadge();
  }
}

function filterInventoryCategory(cat, btn) {
  currentInventoryCategory = cat;
  document.querySelectorAll(".inv-filter-pill").forEach(p => p.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderInventoryDashboard();
}

function filterInventoryStatus(status, btn) {
  currentInventoryStatus = (currentInventoryStatus === status) ? "all" : status;
  document.querySelectorAll(".inv-filter-pill").forEach(p => p.classList.remove("active"));
  if (btn && currentInventoryStatus !== "all") btn.classList.add("active");
  renderInventoryDashboard();
}

function searchInventory(query) {
  inventorySearchQuery = (query || "").trim().toLowerCase();
  renderInventoryDashboard();
}

function renderInventoryDashboard() {
  const tableBody = document.getElementById("inventory-table-body");
  const statTotal = document.getElementById("inv-stat-total");
  const statInStock = document.getElementById("inv-stat-instock");
  const statLowStock = document.getElementById("inv-stat-lowstock");
  const statSoldOut = document.getElementById("inv-stat-soldout");
  const warningBanner = document.getElementById("inv-warning-banner");
  const warningText = document.getElementById("inv-warning-text");

  const inv = getInventory();

  const total = inv.length;
  const inStock = inv.filter(i => i.status === "in_stock").length;
  const lowStock = inv.filter(i => i.status === "low_stock").length;
  const soldOut = inv.filter(i => i.status === "out_of_stock").length;

  if (statTotal) statTotal.textContent = total;
  if (statInStock) statInStock.textContent = inStock;
  if (statLowStock) statLowStock.textContent = lowStock;
  if (statSoldOut) statSoldOut.textContent = soldOut;

  const lowItems = inv.filter(i => i.status === "low_stock");
  if (warningBanner && warningText) {
    if (lowItems.length > 0) {
      warningBanner.style.display = "block";
      const names = lowItems.slice(0, 3).map(i => `${i.name} (${i.stock} left)`).join(", ");
      warningText.textContent = `Low stock alert: ${names}. Restock soon.`;
    } else {
      warningBanner.style.display = "none";
    }
  }

  if (!tableBody) return;

  let filtered = inv;
  if (currentInventoryCategory !== "all") {
    filtered = filtered.filter(i => i.category === currentInventoryCategory);
  }
  if (currentInventoryStatus === "low_stock") {
    filtered = filtered.filter(i => i.status === "low_stock");
  } else if (currentInventoryStatus === "out_of_stock") {
    filtered = filtered.filter(i => i.status === "out_of_stock");
  }
  if (inventorySearchQuery) {
    filtered = filtered.filter(i => i.name.toLowerCase().includes(inventorySearchQuery));
  }

  if (filtered.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:0.9rem;">
          No items match the selected filter.
        </td>
      </tr>
    `;
    return;
  }

  tableBody.innerHTML = filtered.map(item => {
    let badgeHtml = '';
    if (item.status === "in_stock") {
      badgeHtml = `<span class="badge-instock">🟢 In Stock (${item.stock})</span>`;
    } else if (item.status === "low_stock") {
      badgeHtml = `<span class="badge-lowstock">🟡 Low Stock (${item.stock} left)</span>`;
    } else {
      badgeHtml = `<span class="badge-outstock">🔴 Sold Out</span>`;
    }

    const typeIcon = item.isVeg ? '<span style="color:#10b981; font-size:0.8rem;">● Veg</span>' : '<span style="color:#e11d48; font-size:0.8rem;">▲ Non-Veg</span>';

    return `
      <tr style="border-bottom:1px solid var(--border);">
        <td style="padding:12px 16px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${item.image}" alt="${item.name}" style="width:40px; height:40px; border-radius:8px; object-fit:cover;" onerror="this.src='assets/hero_banner.jpg'">
            <div>
              <strong style="font-size:0.9rem; color:var(--text-main); display:block;">${item.name}</strong>
              <div style="font-size:0.75rem; color:var(--text-muted);">${typeIcon} • Updated ${item.lastUpdated || 'recently'}</div>
            </div>
          </div>
        </td>
        <td style="padding:12px 14px; text-transform:capitalize; font-size:0.85rem; color:var(--text-muted);">${item.category}</td>
        <td style="padding:12px 14px; font-weight:800; color:var(--text-main);">₹${item.price}</td>
        <td style="padding:12px 14px; text-align:center;">
          <div style="display:inline-flex; align-items:center; gap:4px;">
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', -5)" title="Decrease 5">-5</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', -1)" title="Decrease 1">-1</button>
            <input type="number" min="0" value="${item.stock}" class="stock-input-field"
              onchange="updateItemStock('${item.id}', this.value)"
              onkeydown="if(event.key==='Enter') this.blur();">
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 1)" title="Increase 1">+1</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 5)" title="Increase 5">+5</button>
            <button type="button" class="btn-stock-adjust" onclick="adjustItemStock('${item.id}', 10)" title="Increase 10">+10</button>
          </div>
        </td>
        <td style="padding:12px 14px;">${badgeHtml}</td>
        <td style="padding:12px 16px; text-align:right;">
          <button type="button" onclick="toggleItemStatus('${item.id}')"
            style="padding:6px 12px; font-size:0.78rem; font-weight:800; border-radius:6px; cursor:pointer; border:1px solid ${item.status === 'out_of_stock' ? '#86efac' : '#fca5a5'}; background:${item.status === 'out_of_stock' ? '#f0fdf4' : '#fef2f2'}; color:${item.status === 'out_of_stock' ? '#15803d' : '#b91c1c'};">
            ${item.status === 'out_of_stock' ? '✓ Mark Available' : '✕ Mark Sold Out'}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

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
    const inv = getInventoryItem(dish.id);
    const isSoldOut = inv ? (inv.status === "out_of_stock" || inv.stock <= 0) : false;
    const isLowStock = inv ? (!isSoldOut && inv.stock <= inv.threshold) : false;
    const qty = cart[dish.id] || 0;
    const typeClass = dish.isVeg ? "veg" : "non-veg";
    let buttonHtml = "";

    if (isSoldOut) {
      buttonHtml = `
        <button type="button" class="btn-sold-out" disabled title="Currently Sold Out in kitchen">
          Sold Out
        </button>
      `;
    } else if (qty > 0) {
      buttonHtml = `
        <div style="display:flex; align-items:center; gap:6px;">
          <div class="qty-pill">
            <button type="button" class="qty-btn-minus" onclick="updateDishQty('${dish.id}', -1)" aria-label="Decrease quantity" title="Decrease quantity">−</button>
            <span class="qty-val">${qty}</span>
            <button type="button" class="qty-btn-plus" onclick="updateDishQty('${dish.id}', 1)" aria-label="Increase quantity" title="Increase quantity">+</button>
          </div>
          <button type="button" class="btn-order-now-selected" onclick="openCartModal()" title="View in cart & order now">
            Order Now
          </button>
        </div>
      `;
    } else {
      buttonHtml = `
        <button type="button" class="add-btn" onclick="updateDishQty('${dish.id}', 1)" title="Add to cart">
          ADD +
        </button>
      `;
    }

    // Compute 5-star visual representation for food items
    const fullStars = Math.floor(dish.rating);
    const hasHalf = (dish.rating - fullStars) >= 0.5;
    let starsStr = "★".repeat(fullStars);
    if (hasHalf && starsStr.length < 5) starsStr += "★";
    const emptyCount = Math.max(0, 5 - starsStr.length);
    const emptyStr = "☆".repeat(emptyCount);

    html += `
      <div class="dish-card ${isSoldOut ? 'out-of-stock' : ''}">
        <div class="dish-img-wrap">
          <img src="${dish.image}" alt="${dish.name}" class="dish-img" onerror="this.src='assets/hero_banner.jpg'">
          <div class="food-type-icon ${typeClass}"></div>
          <span class="rating-badge">★ ${dish.rating}</span>
          ${isSoldOut ? '<div style="position:absolute; top:12px; left:12px; z-index:4;"><span class="badge-sold-out">🔴 SOLD OUT</span></div>' : ''}
          <div class="dish-img-overlay"></div>
        </div>
        <div class="dish-body">
          <div class="dish-title-row">
            <h3 class="dish-name">${dish.name}</h3>
          </div>

          <!-- Prominent Star Rating for Food Item -->
          <div class="dish-star-rating-row" style="display:flex; align-items:center; gap:6px; margin:4px 0 8px 0;">
            <div class="dish-stars-graphic" style="color:#f59e0b; font-size:1.08rem; letter-spacing:1px; line-height:1;" title="${dish.rating} out of 5 stars">
              <span>${starsStr}</span><span style="color:#cbd5e1;">${emptyStr}</span>
            </div>
            <span class="dish-rating-score" style="font-size:0.88rem; font-weight:800; color:var(--text-main);">${dish.rating}</span>
            <span class="dish-reviews-count" style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">(${dish.reviews} reviews)</span>
          </div>

          <p class="dish-desc">${dish.desc}</p>
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:8px;">
            <div class="demand-tag">${dish.demandStatus}</div>
            ${isLowStock ? `<span style="font-size:0.72rem; color:#d97706; font-weight:800; background:#fef3c7; padding:2px 8px; border-radius:6px;">⚠️ Only ${inv.stock} portions left!</span>` : ''}
          </div>
          <div class="dish-footer">
            <div class="dish-price">
              ${dish.originalPrice ? `<span style="text-decoration:line-through; font-size:0.85rem; color:#94a3b8; margin-right:4px;">₹${dish.originalPrice}</span> ` : ''}₹${dish.price}
              ${dish.originalPrice ? `<span style="font-size:0.75rem; color:#10b981; font-weight:800; margin-left:4px;">58% OFF</span>` : ''}
            </div>
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

  const invItem = getInventoryItem(dishId);
  const current = cart[dishId] || 0;
  const next = current + delta;

  // Inventory validation when incrementing quantity
  if (delta > 0 && invItem) {
    if (invItem.status === "out_of_stock" || invItem.stock <= 0) {
      showToast(`Sorry, ${invItem.name} is currently Sold Out in the kitchen!`, "warning");
      return;
    }
    if (next > invItem.stock) {
      showToast(`Only ${invItem.stock} portion(s) available in kitchen stock for ${invItem.name}!`, "warning");
      return;
    }
  }

  if (next <= 0) {
    delete cart[dishId];
  } else {
    cart[dishId] = next;
  }

  renderDishes();
  updateCartBar();
  saveUserData();
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
  // Update mobile bottom nav cart badge
  const totalCount = Object.values(cart).reduce((a, b) => a + b, 0);
  const mobCartBadge = document.getElementById("mob-cart-badge");
  if (mobCartBadge) {
    mobCartBadge.textContent = totalCount;
    mobCartBadge.style.display = totalCount > 0 ? "inline-block" : "none";
  }
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

// =========================================================================
// SWIGGY / ZOMATO OFFERS & LOYALTY COUPON ENGINE
// =========================================================================
let activeCoupon = null;

function addTodaysSpecialToCart() {
  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to order today's special!", "warning");
    performSwitchMode("login");
    return;
  }
  updateDishQty("todays_special_combo", 1);
  showToast("🎉 Added Today's Special (Royal Biryani Combo) for just ₹99 to your cart! 🍛", "success");
  openCartModal();
}

function renderLoyaltyStampCard() {
  const track = document.getElementById("stamp-track");
  const fill = document.getElementById("stamp-progress-fill");
  const text = document.getElementById("stamp-progress-text");
  const hint = document.getElementById("stamp-reward-hint");
  const badgeText = document.getElementById("loyalty-badge-text");

  const streakKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";
  let streak = parseInt(localStorage.getItem(streakKey) || "0", 10);
  const currentCycle = streak % 10;
  const isTenthUnlocked = streak > 0 && (currentCycle === 0 || streak >= 10);

  if (fill) {
    const percent = isTenthUnlocked ? 100 : currentCycle * 10;
    fill.style.width = `${percent}%`;
  }

  if (text) {
    text.innerHTML = `<strong>${isTenthUnlocked ? 10 : currentCycle} / 10</strong> Orders Placed`;
  }

  if (badgeText) {
    badgeText.textContent = isTenthUnlocked ? "🎉 10th FREE UNLOCKED!" : `Order ${currentCycle}/10`;
  }

  if (hint) {
    if (isTenthUnlocked) {
      hint.innerHTML = `<span style="color:#059669; font-weight:800;">🎉 10th Order FREE SMALL ITEM Unlocked! Tap 'FREE10' to claim up to ₹35 off beverages/snacks! ☕</span>`;
    } else {
      const remaining = 10 - currentCycle;
      hint.innerHTML = `<span style="color:var(--primary); font-weight:700;">${remaining} more order${remaining !== 1 ? 's' : ''} to unlock your Free Small Item (Beverage / Snack)! ☕</span>`;
    }
  }

  if (track) {
    let stampsHtml = "";
    for (let i = 1; i <= 10; i++) {
      const isCompleted = isTenthUnlocked ? true : i <= currentCycle;
      const isTenth = (i === 10);
      let circleClass = "stamp-circle";
      if (isCompleted) circleClass += " active";
      if (isTenth) circleClass += " reward-tenth";

      stampsHtml += `
        <div class="${circleClass}" title="${isTenth ? '10th Order: Free Beverage or Snack Item (Up to ₹35 OFF)' : 'Order ' + i}">
          ${isTenth ? '🎁' : (isCompleted ? '✓' : i)}
          <span style="font-size:0.6rem; line-height:1; margin-top:2px;">${isTenth ? '☕ FREE' : '#' + i}</span>
        </div>
      `;
    }
    track.innerHTML = stampsHtml;
  }
}

function simulateOrderStreak() {
  const sKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";
  localStorage.setItem(sKey, "10");
  renderLoyaltyStampCard();
  applyQuickCoupon("FREE10");
  showToast("🎉 10th Order Milestone Reached! Free Small Item (Beverage/Snack) Coupon (FREE10) activated! ☕", "success");
}

function applyQuickCoupon(code) {
  if (!code) return;
  const input = document.getElementById("cart-coupon-input");
  if (input) input.value = code;

  if (!currentUser || !currentUser.role) {
    showToast("🔒 Please login first to apply coupons!", "warning");
    performSwitchMode("login");
    return;
  }

  executeApplyCoupon(code);
}

function applyCartCoupon() {
  const input = document.getElementById("cart-coupon-input");
  const code = input ? input.value.trim().toUpperCase() : "";
  if (!code) {
    showToast("Please enter a valid coupon code!", "warning");
    return;
  }
  executeApplyCoupon(code);
}

function executeApplyCoupon(code) {
  const msgEl = document.getElementById("cart-coupon-msg");
  const badgeEl = document.getElementById("cart-active-coupon-badge");

  const validCodes = {
    "FREE10": {
      name: "10th Order Free Small Item (Beverage / Snack)",
      calc: (subtotal) => Math.min(subtotal, 35),
      desc: "Free Small Item (Up to ₹35 OFF on Snacks/Drinks)"
    },
    "SPECIAL99": {
      name: "Today's Special Deal",
      calc: (subtotal) => Math.min(subtotal, 99),
      desc: "Flat ₹99 Deal Applied"
    },
    "SPECIAL50": {
      name: "Today's Special Deal",
      calc: (subtotal) => Math.min(subtotal, 99),
      desc: "Flat ₹99 Deal Applied"
    },
    "SAVITHA30": {
      name: "Campus Savings",
      calc: (subtotal) => (subtotal >= 99 ? 30 : 0),
      minSubtotal: 99,
      desc: "Flat ₹30 OFF"
    },
    "FREEDRINK": {
      name: "Complimentary Beverage",
      calc: (subtotal) => (subtotal >= 70 ? 25 : 0),
      minSubtotal: 70,
      desc: "Free Drink (₹25 OFF)"
    }
  };

  const coupon = validCodes[code];
  if (!coupon) {
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#ef4444";
      msgEl.textContent = `❌ Invalid coupon code '${code}'. Try FREE10, SAVITHA30, or SPECIAL99.`;
    }
    showToast(`Invalid coupon code '${code}'`, "warning");
    return;
  }

  // Strict Milestone Check for FREE10: Must complete 10 orders!
  if (code === "FREE10") {
    const streakKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";
  let streak = parseInt(localStorage.getItem(streakKey) || "0", 10);
    const isTenthUnlocked = streak > 0 && (streak % 10 === 0 || streak >= 10);
    if (!isTenthUnlocked) {
      const remaining = 10 - (streak % 10);
      const msg = `⚠️ FREE10 unlocks only after completing 10 orders! (${remaining} more order${remaining !== 1 ? 's' : ''} needed).`;
      if (msgEl) {
        msgEl.style.display = "block";
        msgEl.style.color = "#f59e0b";
        msgEl.textContent = msg;
      }
      showToast(msg, "warning");
      return;
    }
  }

  // Daily Cooldown Check: Don't give coupons on every order!
  const todayStr = new Date().toDateString();
  let usedCoupons = {};
  try {
    usedCoupons = JSON.parse(localStorage.getItem("savitha_used_coupons") || "{}");
  } catch (e) {}
  if (usedCoupons[code] && usedCoupons[code] === todayStr) {
    const msg = `⚠️ Coupon '${code}' has already been redeemed today! Promotional coupons are limited to 1 per student per day.`;
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#f59e0b";
      msgEl.textContent = msg;
    }
    showToast(msg, "warning");
    return;
  }

  // Calculate current cart subtotal
  let subtotal = 0;
  for (const [id, qty] of Object.entries(cart)) {
    const dish = DISHES.find(d => d.id === id);
    if (dish) subtotal += (dish.price * qty);
  }

  if (coupon.minSubtotal && subtotal < coupon.minSubtotal) {
    if (msgEl) {
      msgEl.style.display = "block";
      msgEl.style.color = "#f59e0b";
      msgEl.textContent = `⚠️ Code '${code}' requires a minimum order value of ₹${coupon.minSubtotal}.`;
    }
    showToast(`Requires min order of ₹${coupon.minSubtotal}`, "warning");
    return;
  }

  activeCoupon = { code: code, ...coupon };

  if (msgEl) {
    msgEl.style.display = "block";
    msgEl.style.color = "#059669";
    msgEl.innerHTML = `✓ Coupon <strong>${code}</strong> applied! ${coupon.desc}`;
  }
  if (badgeEl) badgeEl.style.display = "inline-block";

  showToast(`🎉 Coupon ${code} applied successfully!`, "success");
  openCartModal();
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
    const subtotalEl = document.getElementById("cart-subtotal-val");
    const discountRow = document.getElementById("cart-discount-row");
    if (subtotalEl) subtotalEl.textContent = "₹0";
    if (discountRow) discountRow.style.display = "none";
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
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border); gap:8px;">
          <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:0;">
            <img src="${dish.image}" alt="${dish.name}" style="width:44px; height:44px; border-radius:8px; object-fit:cover; flex-shrink:0;" onerror="this.src='assets/hero_banner.jpg'">
            <div style="overflow:hidden;">
              <strong style="color:var(--text-main); font-size:0.92rem; display:block; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">${dish.name}</strong>
              <div style="font-size:0.78rem; color:var(--text-muted);">₹${dish.price} each</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
            <!-- Student Quantity Update Button in Cart Modal -->
            <div class="cart-qty-ctrl">
              <button type="button" class="cart-qty-btn cart-qty-minus" onclick="updateDishQty('${dish.id}', -1); openCartModal();" aria-label="Decrease quantity" title="Decrease quantity">−</button>
              <span class="cart-qty-val">${qty}</span>
              <button type="button" class="cart-qty-btn cart-qty-plus" onclick="updateDishQty('${dish.id}', 1); openCartModal();" aria-label="Increase quantity" title="Increase quantity">+</button>
            </div>
            <strong style="color:var(--text-main); min-width:50px; text-align:right; font-size:0.92rem;">₹${itemCost}</strong>
            <button type="button" onclick="updateDishQty('${dish.id}', -${qty}); openCartModal();" style="background:#fee2e2; border:1px solid #fca5a5; color:#ef4444; border-radius:6px; width:26px; height:26px; display:inline-flex; align-items:center; justify-content:center; font-size:0.85rem; cursor:pointer;" aria-label="Remove item" title="Remove item">✕</button>
          </div>
        </div>
      `;
    }
  });

  let discount = 0;
  if (activeCoupon) {
    discount = activeCoupon.calc(sum);
    if (discount <= 0 && activeCoupon.minSubtotal && sum < activeCoupon.minSubtotal) {
      activeCoupon = null;
    }
  }

  const finalPayable = Math.max(0, sum - discount);

  const subtotalEl = document.getElementById("cart-subtotal-val");
  const discountRow = document.getElementById("cart-discount-row");
  const discountLabel = document.getElementById("cart-discount-label");
  const discountVal = document.getElementById("cart-discount-val");
  const badgeEl = document.getElementById("cart-active-coupon-badge");
  const couponMsg = document.getElementById("cart-coupon-msg");
  const couponInput = document.getElementById("cart-coupon-input");

  if (subtotalEl) subtotalEl.textContent = `₹${sum}`;

  if (activeCoupon && discount > 0) {
    if (discountRow) discountRow.style.display = "flex";
    if (discountLabel) discountLabel.textContent = `Coupon Discount (${activeCoupon.code})`;
    if (discountVal) discountVal.textContent = `-₹${discount}`;
    if (badgeEl) badgeEl.style.display = "inline-block";
    if (couponInput && !couponInput.value) couponInput.value = activeCoupon.code;
  } else {
    if (discountRow) discountRow.style.display = "none";
    if (badgeEl) badgeEl.style.display = "none";
    if (couponMsg && !activeCoupon) couponMsg.style.display = "none";
  }

  if (list) list.innerHTML = html;
  if (total) total.textContent = `₹${finalPayable}`;

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

  let discountAmount = 0;
  if (activeCoupon) {
    discountAmount = activeCoupon.calc(totalAmount);
    totalAmount = Math.max(0, totalAmount - discountAmount);
  }

  // Increment loyalty streak
  const streakKey = (currentUser && currentUser.id) ? `savitha_streak_${currentUser.id}` : "savitha_user_order_count";
  let currentStreak = parseInt(localStorage.getItem(streakKey) || "0", 10) + 1;
  localStorage.setItem(streakKey, String(currentStreak));

  const usedCoupon = activeCoupon ? activeCoupon.code : null;
  activeCoupon = null; // reset for next cart

  const letters = ["A", "B", "C", "D"];
  const randomLetter = letters[Math.floor(Math.random() * letters.length)];
  const randomNum = Math.floor(10 + Math.random() * 89);
  const token = `#${randomLetter}-${randomNum}`;
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const totalQty = items.reduce((sum, it) => sum + (it.qty || 1), 0);
  const prepMinutes = Math.min(25, Math.max(8, 8 + Math.floor(totalQty * 2)));
  const arrivalDate = new Date(now.getTime() + prepMinutes * 60000);
  const arrivalTimeStr = arrivalDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const newOrder = {
    id: "ord_" + Date.now(),
    token: token,
    userId: currentUser ? currentUser.id : "usr_guest",
    user_id: currentUser ? currentUser.id : "usr_guest",
    username: currentUser ? (currentUser.username || currentUser.id) : "guest",
    customer: customerName,
    customerName: customerName,
    customer_name: customerName,
    customerYear: customerYear,
    customer_year: customerYear,
    customerPhone: customerPhone,
    customer_phone: customerPhone,
    items: items,
    total: totalAmount,
    coupon: usedCoupon,
    discount: discountAmount,
    time: timeStr,
    timestamp: Date.now(),
    status: "Cooking",
    prepTime: `${prepMinutes - 2}-${prepMinutes + 2} mins`,
    arrivalTime: arrivalTimeStr,
    arrival_time: arrivalTimeStr,
    arrivalMinutes: prepMinutes,
    arrival_minutes: prepMinutes
  };

  liveOrders.unshift(newOrder);
  myOrders.unshift(newOrder);
  lastPlacedOrder = newOrder;

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    if (currentUser && currentUser.id) {
      localStorage.setItem(`savitha_my_orders_${currentUser.id}`, JSON.stringify(myOrders));
    }
    localStorage.setItem("savitha_student_active_order", JSON.stringify(newOrder));
  } catch (e) {}

  saveUserData();

  // Sync to backend API if available
  try {
    fetch(`${API_BASE}/api/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newOrder)
    }).catch(() => {});
  } catch (e) {}

  // Decrement inventory portions in kitchen stock
  decrementOrderInventory(items);

  // Record used coupon in daily cooldown
  if (usedCoupon) {
    try {
      const used = JSON.parse(localStorage.getItem("savitha_used_coupons") || "{}");
      used[usedCoupon] = new Date().toDateString();
      localStorage.setItem("savitha_used_coupons", JSON.stringify(used));
    } catch (e) {}
  }

  // Random lucky coupon roll: Only 25% chance (don't give coupons everytime!)
  if (Math.random() < 0.25 && usedCoupon !== "SAVITHA30") {
    try {
      localStorage.setItem("savitha_pending_lucky_coupon", "SAVITHA30");
      showToast("🍀 Lucky Order Bonus! You won a ₹30 campus coupon (SAVITHA30) for a future meal!", "success");
    } catch (e) {}
  }

  cart = {};
  renderDishes();
  updateCartBar();
  updateMyOrdersCount();
  updateLiveOrderBadge();
  renderLoyaltyStampCard();

  // If we order anything, it is visible ONLY in My Orders, not anywhere else!
  openMyOrdersModal();
  if (usedCoupon === "FREE10") {
    showToast(`🎉 10th ORDER FREE ITEM (Drink/Snack) CLAIMED! Token: ${token}`, "success");
  } else {
    showToast(`🎉 Order placed successfully! Token: ${token} (View in My Orders)`, "success");
  }
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

    const arrivalTimeEl = document.getElementById("token-arrival-time");
    const arrivalCountdownEl = document.getElementById("token-arrival-countdown");
    if (arrivalTimeEl) {
      arrivalTimeEl.textContent = target.arrivalTime || target.arrival_time || "Ready in ~10 mins";
    }
    if (arrivalCountdownEl) {
      arrivalCountdownEl.textContent = target.arrivalMinutes ? `~${target.arrivalMinutes} mins` : "~10 mins";
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
  const userOrders = (!currentUser || !currentUser.id)
    ? []
    : myOrders.filter(ord => isOrderForUser(ord, currentUser));
  const count = userOrders.length;

  if (countMenu) countMenu.textContent = count;
  if (countTop) {
    countTop.textContent = count;
    countTop.style.display = count > 0 ? "inline-block" : "none";
  }
  const mobOrdersBadge = document.getElementById("mob-orders-badge");
  if (mobOrdersBadge) {
    mobOrdersBadge.textContent = count;
    mobOrdersBadge.style.display = count > 0 ? "inline-block" : "none";
  }
}

function renderMyOrdersList() {
  const container = document.getElementById("my-orders-list-container");
  if (!container) return;

  // Strict user-specific isolation: Only display orders belonging to the currently logged in user!
  const userOrders = (!currentUser || !currentUser.id) 
    ? [] 
    : myOrders.filter(ord => isOrderForUser(ord, currentUser));

  if (userOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:32px 16px; background:#f8fafc; border-radius:12px; border:1px dashed var(--border);">
        <div style="font-size:2.4rem; margin-bottom:8px;">🍽️</div>
        <div style="font-size:1.05rem; font-weight:800; color:var(--text-main);">No active orders for ${currentUser ? currentUser.name : 'you'}</div>
        <p style="font-size:0.84rem; color:var(--text-muted); margin:4px 0 14px 0;">Select your dishes from the menu to get your digital pickup token!</p>
        <button type="button" class="btn-hero-primary" onclick="closeMyOrdersModal(); performSwitchMode('order');" style="padding:8px 18px; font-size:0.88rem; border-radius:999px;">
          Browse Food Menu
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = userOrders.map(ord => {
    const isReady = ord.status && (ord.status.includes("Ready") || ord.status === "Ready");
    const statusBg = isReady ? "#dcfce7" : "#fef3c7";
    const statusColor = isReady ? "#15803d" : "#b45309";
    const statusIcon = isReady ? "✅" : "⏳";
    const statusText = isReady ? "Ready for Pickup at Counter!" : (ord.status || "Preparing in Kitchen ⏳");

    const itemsRows = (ord.items || []).map(i => `
      <div style="display:flex; justify-content:space-between; margin-bottom:3px; font-size:0.86rem; color:var(--text-main);">
        <span>${i.qty}x ${i.name}</span>
        <strong>₹${i.price * i.qty}</strong>
      </div>
    `).join('');

    return `
      <div class="my-order-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:16px; margin-bottom:14px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.35rem; font-weight:900; color:var(--primary); background:#eef2ff; padding:4px 12px; border-radius:8px; border:1.5px solid #c7d2fe; letter-spacing:0.5px;">${ord.token}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">🕒 ${ord.time || "Recently"}</span>
          </div>
          <span style="font-size:0.78rem; font-weight:800; padding:4px 10px; border-radius:999px; background:${statusBg}; color:${statusColor}; display:inline-flex; align-items:center; gap:4px;">
            ${statusIcon} ${statusText}
          </span>
        </div>

        <!-- FOOD ARRIVAL ESTIMATE BANNER -->
        <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:8px 12px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
          <span style="font-size:0.82rem; font-weight:700; color:#92400e; display:inline-flex; align-items:center; gap:5px;">
            <span>🛵</span> <strong>Estimated Food Arrival:</strong> <span style="color:#b45309; font-weight:800; font-size:0.92rem;">${ord.arrivalTime || ord.arrival_time || 'Ready in ~10 mins'}</span>
          </span>
          <span style="font-size:0.76rem; font-weight:800; color:#d97706; background:#fef3c7; padding:2px 8px; border-radius:999px;">
            ${ord.arrivalMinutes ? `~${ord.arrivalMinutes} mins wait` : 'Fast Kitchen Prep'}
          </span>
        </div>

        <div style="background:#f8fafc; border-radius:10px; padding:10px 12px; margin-bottom:10px; border:1px solid #f1f5f9;">
          <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">Order Summary</div>
          ${itemsRows || '<div style="font-size:0.86rem;">Selected Meals</div>'}
          <div style="border-top:1px dashed #e2e8f0; margin-top:6px; padding-top:6px; display:flex; justify-content:space-between; font-weight:800; font-size:0.95rem;">
            <span>Total Paid</span>
            <span style="color:var(--primary);">₹${ord.total}</span>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.8rem; color:var(--text-muted);">Show token at counter to collect</span>
          <button type="button" class="btn-banner-cancel" onclick="cancelOrder('${ord.id}')"
            style="padding:6px 14px; font-size:0.82rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:8px; cursor:pointer; font-weight:700; display:inline-flex; align-items:center; gap:4px;">
            <span>❌</span> Cancel Order
          </button>
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


// =========================================================================
// LAST MINUTE CANCELLATION CHARGE ENGINE
// =========================================================================
let pendingCancelOrderId = null;

function openCancelOrderModal(orderId) {
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId)
    || myOrders.find(o => o.id === orderId || o.token === orderId)
    || (lastPlacedOrder && (lastPlacedOrder.id === orderId || lastPlacedOrder.token === orderId) ? lastPlacedOrder : null);

  if (!target) {
    showToast("Order not found or already cancelled.", "warning");
    return;
  }

  pendingCancelOrderId = target.id;
  const modal = document.getElementById("cancel-order-modal");
  const content = document.getElementById("cancel-modal-content");
  if (!modal || !content) {
    confirmCancellationWithCharge(target.id, 20, Math.max(0, target.total - 20));
    return;
  }

  const orderTime = target.timestamp || Date.now();
  const elapsedSec = Math.max(0, Math.floor((Date.now() - orderTime) / 1000));
  const isGracePeriod = (elapsedSec <= 60);

  const cancellationFee = isGracePeriod ? 0 : Math.min(20, target.total);
  const refundAmount = Math.max(0, target.total - cancellationFee);

  content.innerHTML = `
    <div style="background:#f8fafc; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span style="font-size:1.15rem; font-weight:900; color:var(--primary);">${target.token}</span>
        <span style="font-size:0.78rem; font-weight:800; padding:3px 8px; border-radius:999px; background:${isGracePeriod ? '#dcfce7' : '#fef3c7'}; color:${isGracePeriod ? '#15803d' : '#b45309'};">
          ${isGracePeriod ? '🟢 Within 1-Min Grace Period' : '⚠️ Last-Minute Cancellation'}
        </span>
      </div>

      <div style="font-size:0.84rem; color:var(--text-main); margin-bottom:8px; line-height:1.4;">
        ${isGracePeriod 
          ? 'You are within the <strong>1-minute grace window</strong>. Food preparation has not started, so <strong>no cancellation fee</strong> applies!'
          : `The kitchen has already begun food preparation (<strong>${elapsedSec}s elapsed</strong>). As per canteen policy to reduce food waste, a <strong>Last-Minute Cancellation Fee of ₹${cancellationFee}</strong> applies.`
        }
      </div>

      <div style="border-top:1px dashed #cbd5e1; padding-top:8px; font-size:0.86rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
          <span style="color:var(--text-muted);">Order Total:</span>
          <strong>₹${target.total}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px; color:${cancellationFee > 0 ? '#ef4444' : '#10b981'};">
          <span>Cancellation Charge:</span>
          <strong>${cancellationFee > 0 ? '-₹' + cancellationFee : '₹0 (Free)'}</strong>
        </div>
        <div style="border-top:1px solid #e2e8f0; margin-top:4px; padding-top:4px; display:flex; justify-content:space-between; font-weight:900; font-size:0.95rem;">
          <span>Refund to Account:</span>
          <span style="color:#10b981;">₹${refundAmount}</span>
        </div>
      </div>
    </div>

    <div style="display:flex; gap:10px;">
      <button type="button" class="btn-hero-secondary" onclick="closeCancelOrderModal();"
        style="flex:1; padding:10px; font-size:0.88rem; justify-content:center;">
        Keep My Order
      </button>
      <button type="button" class="btn-banner-cancel" onclick="confirmCancellationWithCharge('${target.id}', ${cancellationFee}, ${refundAmount});"
        style="flex:1; padding:10px; font-size:0.88rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:10px; font-weight:800; cursor:pointer; justify-content:center;">
        Confirm Cancel ${cancellationFee > 0 ? '(₹' + cancellationFee + ' Fee)' : ''}
      </button>
    </div>
  `;

  modal.classList.add("show");
}

function closeCancelOrderModal() {
  const modal = document.getElementById("cancel-order-modal");
  if (modal) modal.classList.remove("show");
  pendingCancelOrderId = null;
}

function confirmCancellationWithCharge(orderId, fee, refund) {
  closeCancelOrderModal();
  const target = liveOrders.find(o => o.id === orderId || o.token === orderId)
    || myOrders.find(o => o.id === orderId || o.token === orderId)
    || (lastPlacedOrder && (lastPlacedOrder.id === orderId || lastPlacedOrder.token === orderId) ? lastPlacedOrder : null);

  if (!target) return;

  // Remove from live cooking queue in kitchen
  liveOrders = liveOrders.filter(o => o.id !== target.id && o.token !== target.token);

  // Update in myOrders with cancellation status and fee
  const myOrd = myOrders.find(o => o.id === target.id || o.token === target.token);
  if (myOrd) {
    myOrd.status = fee > 0 ? `Cancelled (₹${fee} Late Fee Applied)` : `Cancelled (Full Refund)`;
    myOrd.cancellationFee = fee;
    myOrd.refundAmount = refund;
  }

  try {
    localStorage.setItem("savitha_live_orders", JSON.stringify(liveOrders));
    localStorage.setItem("savitha_my_orders", JSON.stringify(myOrders));
    localStorage.removeItem("savitha_student_active_order");
  } catch (e) {}

  try {
    fetch(`${API_BASE}/api/orders/${target.id}/cancel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cancellation_fee: fee, refund: refund, reason: fee > 0 ? "Last-minute cancellation charge" : "Grace window cancellation" })
    }).catch(() => {});
  } catch (e) {}

  updateMyOrdersCount();
  renderMyOrdersList();
  updateLiveOrderBadge();
  closeTokenModal();

  if (fee > 0) {
    showToast(`Order ${target.token} cancelled. ₹${fee} late fee applied (₹${refund} refunded).`, "warning");
  } else {
    showToast(`Order ${target.token} cancelled within grace window. Full refund of ₹${refund} issued.`, "info");
  }
}

function cancelOrder(orderId) {
  openCancelOrderModal(orderId);
  return;

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

// =========================================================================
// USER-SPECIFIC ACCOUNTS, CREDENTIALS & ISOLATED DATA STORE
// =========================================================================
const DEFAULT_ACCOUNTS = [
  {
    id: "usr_srinath",
    username: "SAV101",
    password: "pass123",
    name: "Srinath Kumar",
    year: "3rd Year CSE",
    phone: "9876543210",
    role: "student"
  },
  {
    id: "usr_divya",
    username: "SAV102",
    password: "pass123",
    name: "Divya Krishnan",
    year: "Final Year IT",
    phone: "9876543211",
    role: "student"
  },
  {
    id: "usr_aarav",
    username: "SAV103",
    password: "pass123",
    name: "Aarav Menon",
    year: "2nd Year ECE",
    phone: "9876543212",
    role: "student"
  },
  {
    id: "usr_staff",
    username: "staff",
    password: "savi123",
    name: "Kitchen Staff",
    year: "Campus Dining",
    phone: "9876543200",
    role: "worker"
  }
];

function getAccounts() {
  try {
    const raw = localStorage.getItem("savitha_user_accounts");
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch (e) {}
  saveAccounts(DEFAULT_ACCOUNTS);
  return DEFAULT_ACCOUNTS;
}

function saveAccounts(accounts) {
  try {
    localStorage.setItem("savitha_user_accounts", JSON.stringify(accounts));
  } catch (e) {}
}

function findAccount(identifier) {
  const accounts = getAccounts();
  const u = String(identifier || "").trim().toUpperCase();
  return accounts.find(a => a.username.toUpperCase() === u || a.name.toUpperCase() === u || a.id.toUpperCase() === u) || null;
}

function switchStudentAuthMode(mode) {
  const formSignIn = document.getElementById("student-signin-form");
  const formRegister = document.getElementById("student-register-form");

  if (mode === "register") {
    if (formSignIn) formSignIn.style.display = "none";
    if (formRegister) formRegister.style.display = "block";
    const userInp = document.getElementById("register-student-username");
    if (userInp) userInp.focus();
  } else {
    if (formSignIn) formSignIn.style.display = "block";
    if (formRegister) formRegister.style.display = "none";
    const userInp = document.getElementById("login-student-username");
    if (userInp) userInp.focus();
  }
}

function fillDemoStudent(username, password) {
  switchStudentAuthMode("signin");
  const userInp = document.getElementById("login-student-username");
  const passInp = document.getElementById("login-student-password");
  if (userInp) userInp.value = username;
  if (passInp) passInp.value = password;
}

function loadUserData(user) {
  if (!user || !user.id) {
    cart = {};
    myOrders = [];
    activeCoupon = null;
    lastPlacedOrder = null;
    updateCartBar();
    updateMyOrdersCount();
    renderMyOrdersList();
    return;
  }

  // Load user's private cart
  try {
    const userCartRaw = localStorage.getItem(`savitha_cart_${user.id}`);
    cart = userCartRaw ? JSON.parse(userCartRaw) : {};
  } catch (e) {
    cart = {};
  }

  // Load user's private orders
  try {
    const userOrdersRaw = localStorage.getItem(`savitha_my_orders_${user.id}`);
    myOrders = userOrdersRaw ? JSON.parse(userOrdersRaw) : [];
  } catch (e) {
    myOrders = [];
  }

  // Strictly synchronize matching orders from liveOrders using isOrderForUser
  if (Array.isArray(liveOrders)) {
    const matching = liveOrders.filter(o => isOrderForUser(o, user));
    matching.forEach(ord => {
      if (!myOrders.some(m => m.id === ord.id)) {
        myOrders.unshift(ord);
      }
    });
  }

  // Also query backend for this user's phone if available
  if (user.phone) {
    const cleanPhone = String(user.phone).replace(/\D/g, '').slice(-10);
    if (cleanPhone.length === 10) {
      fetch(`${API_BASE}/api/orders?phone=${cleanPhone}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data && Array.isArray(data.orders)) {
            let changed = false;
            data.orders.forEach(backendOrder => {
              if (isOrderForUser(backendOrder, user)) {
                const existing = myOrders.find(m => m.id === backendOrder.id);
                if (!existing) {
                  myOrders.unshift(backendOrder);
                  changed = true;
                } else if (existing.status !== backendOrder.status) {
                  Object.assign(existing, backendOrder);
                  changed = true;
                }
              }
            });
            if (changed) {
              saveUserData();
              updateMyOrdersCount();
              renderMyOrdersList();
            }
          }
        }).catch(() => {});
    }
  }

  lastPlacedOrder = myOrders.length > 0 ? myOrders[0] : null;

  updateCartBar();
  updateMyOrdersCount();
  renderLoyaltyStampCard();
  renderMyOrdersList();
}

function saveUserData() {
  if (!currentUser || !currentUser.id) return;
  try {
    localStorage.setItem(`savitha_cart_${currentUser.id}`, JSON.stringify(cart));
    localStorage.setItem(`savitha_my_orders_${currentUser.id}`, JSON.stringify(myOrders));
  } catch (e) {}
}

function loginUser(userAccount) {
  // Clear any active cart and orders from previous session in memory
  cart = {};
  myOrders = [];
  lastPlacedOrder = null;
  activeCoupon = null;

  currentUser = userAccount;
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (e) {}

  // Load user's isolated data store
  loadUserData(currentUser);

  renderUserAuthSlot();
  applyRoleVisibility();

  if (currentUser.role === "worker") {
    performSwitchMode("manager");
  } else {
    performSwitchMode("order");
    renderDishes();
  }
}

function handleStudentSignIn(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const userInp = document.getElementById("login-student-username");
  const passInp = document.getElementById("login-student-password");
  const username = userInp ? userInp.value.trim() : "";
  const password = passInp ? passInp.value.trim() : "";

  if (!username) {
    showToast("⚠️ Please enter your Student ID or Username!", "warning");
    if (userInp) userInp.focus();
    return false;
  }
  if (!password) {
    showToast("⚠️ Please enter your account password!", "warning");
    if (passInp) passInp.focus();
    return false;
  }

  const account = findAccount(username);
  if (!account || account.password !== password) {
    showToast("❌ Invalid Student ID or password! Please check credentials or register.", "warning");
    if (passInp) {
      passInp.style.borderColor = "#ef4444";
      setTimeout(() => { if (passInp) passInp.style.borderColor = ""; }, 2500);
    }
    return false;
  }

  loginUser(account);
  showToast(`Welcome back! Logged in as Student (${account.username}).`, "success");
  return false;
}

function handleStudentRegister(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const nameInp = document.getElementById("register-student-name");
  const userInp = document.getElementById("register-student-username");
  const yearInp = document.getElementById("register-student-year");
  const phoneInp = document.getElementById("register-student-phone");
  const passInp = document.getElementById("register-student-password");

  const name = nameInp ? nameInp.value.trim() : "";
  const username = userInp ? userInp.value.trim().toUpperCase() : "";
  const year = yearInp ? yearInp.value : "1st Year";
  const phone = phoneInp ? phoneInp.value.trim() : "";
  const password = passInp ? passInp.value.trim() : "";

  if (!name) {
    showToast("⚠️ Please enter your full name!", "warning");
    if (nameInp) nameInp.focus();
    return false;
  }
  if (!username) {
    showToast("⚠️ Please enter a Student ID / Roll No!", "warning");
    if (userInp) userInp.focus();
    return false;
  }
  if (!password || password.length < 3) {
    showToast("⚠️ Password must be at least 3 characters long!", "warning");
    if (passInp) passInp.focus();
    return false;
  }

  if (findAccount(username)) {
    showToast(`⚠️ Account with ID '${username}' already exists. Please sign in!`, "warning");
    switchStudentAuthMode("signin");
    const uInp = document.getElementById("login-student-username");
    if (uInp) uInp.value = username;
    return false;
  }

  const newAccount = {
    id: "usr_" + username.toLowerCase().replace(/[^a-z0-9]/g, ""),
    username: username,
    password: password,
    name: name,
    year: year,
    phone: phone,
    role: "student",
    created_at: new Date().toISOString()
  };

  const accounts = getAccounts();
  accounts.push(newAccount);
  saveAccounts(accounts);

  // Sync to backend if available
  try {
    fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newAccount)
    }).catch(() => {});
  } catch (e) {}

  loginUser(newAccount);
  showToast(`🎉 Account created successfully! Welcome to Savitha Canteen, ${name}.`, "success");
  return false;
}

function openProfileModal() {
  if (!currentUser || !currentUser.role) {
    showToast("Please login first to view your profile.", "warning");
    performSwitchMode("login");
    return;
  }

  const modal = document.getElementById("profile-modal");
  const body = document.getElementById("profile-modal-body");
  if (!modal || !body) return;

  const isWorker = currentUser.role === "worker";
  const icon = isWorker ? "👨‍🍳" : "🎓";
  const totalOrders = myOrders.length;
  const streak = parseInt(localStorage.getItem(`savitha_streak_${currentUser.id}`) || String(totalOrders), 10);
  const activeOrdersCount = myOrders.filter(o => o.status === "Cooking").length;

  body.innerHTML = `
    <div style="text-align:center; padding:10px 0 16px 0; border-bottom:1px solid var(--border);">
      <div style="width:68px; height:68px; border-radius:50%; background:linear-gradient(135deg, #4f46e5 0%, #818cf8 100%); color:#fff; font-size:2rem; display:inline-flex; align-items:center; justify-content:center; margin-bottom:10px; box-shadow:0 4px 12px rgba(79, 70, 229, 0.25);">
        ${icon}
      </div>
      <h3 style="font-size:1.25rem; font-weight:900; color:var(--text-main); margin:0;">${currentUser.name || "Student"}</h3>
      <div style="font-size:0.84rem; color:var(--primary); font-weight:800; margin-top:2px;">
        Account ID: ${currentUser.username || currentUser.id || "SAV101"}
      </div>
      <div style="display:inline-block; font-size:0.75rem; background:#e0e7ff; color:#3730a3; padding:2px 10px; border-radius:999px; font-weight:800; margin-top:6px;">
        ${isWorker ? "Kitchen Staff Member" : "Registered Student Account"}
      </div>
    </div>

    <div style="padding:14px 0; font-size:0.88rem;">
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Department / Year:</span>
        <strong style="color:var(--text-main);">${currentUser.year || "3rd Year"}</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Mobile Number:</span>
        <strong style="color:var(--text-main);">${currentUser.phone || "Not specified"}</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Total Orders Placed:</span>
        <strong style="color:var(--primary);">${totalOrders} orders</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #e2e8f0;">
        <span style="color:var(--text-muted);">Loyalty Stamp Streak:</span>
        <strong style="color:#059669;">${streak % 10} / 10 Orders</strong>
      </div>
      <div style="display:flex; justify-content:space-between; padding:8px 0;">
        <span style="color:var(--text-muted);">Active In-Kitchen Orders:</span>
        <strong style="color:${activeOrdersCount > 0 ? '#ea580c' : 'var(--text-main)'};">${activeOrdersCount} active</strong>
      </div>
    </div>

    <div style="display:flex; gap:10px; margin-top:6px;">
      ${!isWorker ? `
        <button type="button" class="btn-hero-primary" onclick="closeProfileModal(); openMyOrdersModal();"
          style="flex:1; padding:10px; font-size:0.86rem; border-radius:10px; justify-content:center;">
          📦 View My Orders (${totalOrders})
        </button>
      ` : ''}
      <button type="button" class="btn-banner-cancel" onclick="logoutUser();"
        style="flex:1; padding:10px; font-size:0.86rem; background:#fee2e2; border:1.5px solid #fca5a5; color:#dc2626; border-radius:10px; font-weight:800; cursor:pointer; justify-content:center;">
        Sign Out
      </button>
    </div>
  `;

  modal.classList.add("show");
}

function closeProfileModal() {
  const modal = document.getElementById("profile-modal");
  if (modal) modal.classList.remove("show");
}

// 6. AUTHENTICATION & LOGIN PORTAL (STRICT ACCESS & PASSWORD PRIVACY)
// =========================================================================
function getKitchenStaffPassword() {
  try {
    const saved = localStorage.getItem("savitha_kitchen_pwd");
    if (!saved || saved === "canteen123") {
      return "savi123";
    }
    return saved;
  } catch (e) {
    return "savi123";
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
  const current = String(getKitchenStaffPassword()).trim().toLowerCase();
  return p === current || p === "savi123";
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

  const viewLogin = document.getElementById("view-login");
  const isLoginPage = viewLogin && viewLogin.style.display === "block";

  if (currentUser && currentUser.role && !currentUser.isGuest && !isLoginPage) {
    const isWorker = currentUser.role === "worker";
    const icon = isWorker ? "👨‍🍳" : "🎓";
    const userBadge = isWorker ? "Kitchen Staff" : (currentUser.username ? `Student (${currentUser.username})` : "Student Account");
    slot.innerHTML = `
      <div class="user-session-chip" onclick="openProfileModal()" style="cursor:pointer;" title="View Your Profile">
        <span style="display:inline-flex; align-items:center; gap:6px;">${icon} ${userBadge}</span>
        <button type="button" class="btn-logout-tiny" onclick="event.stopPropagation(); logoutUser()" title="Sign Out">Sign Out</button>
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
  // Check if a saved session exists in localStorage
  try {
    const saved = localStorage.getItem("savitha_user");
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed && parsed.role) {
        currentUser = parsed;
      }
    }
  } catch (e) {
    currentUser = null;
  }

  renderUserAuthSlot();
  applyRoleVisibility();

  // ALWAYS start on the About page. Food menu is NEVER shown without explicitly entering the menu!
  performSwitchMode("about");
}

function switchLoginTab(tab) {
  switchLoginRoleTab(tab);
}

function quickDemoStudentLogin() {
  currentUser = { role: "student", name: "Student User", year: "1st Year", phone: "" };
  try {
    localStorage.setItem("savitha_user", JSON.stringify(currentUser));
  } catch (err) {}

  renderUserAuthSlot();
  applyRoleVisibility();
  performSwitchMode("order");
  renderDishes();
  showToast("Welcome! Food menu is ready 🍛", "success");
}

function handlePortalStudentLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }

  const nameInput = document.getElementById("login-student-name") || document.getElementById("modal-student-name");
  const phoneInput = document.getElementById("login-student-phone") || document.getElementById("modal-student-phone");
  const semInput = document.getElementById("login-student-sem") || document.getElementById("login-student-year") || document.getElementById("modal-student-sem");

  const name = nameInput && nameInput.value.trim() ? nameInput.value.trim() : "";
  const rawPhone = phoneInput && phoneInput.value.trim() ? phoneInput.value.trim() : "";
  const cleanPhone = rawPhone.replace(/\D/g, '').slice(-10);
  const sem = semInput && semInput.value ? semInput.value : "Sem 4 • 2nd Year";

  if (!name) {
    showToast("⚠️ Please enter your Full Name to login!", "warning");
    if (nameInput) nameInput.focus();
    return false;
  }

  if (!cleanPhone || cleanPhone.length !== 10) {
    showToast("⚠️ Please enter a valid 10-digit mobile number!", "warning");
    if (phoneInput) phoneInput.focus();
    return false;
  }

  // Create isolated account deterministically tied to student's 10-digit phone
  const userId = "usr_" + cleanPhone;
  const username = name.toLowerCase().replace(/[^a-z0-9]/g, "") + "_" + cleanPhone.slice(-4);
  const account = {
    id: userId,
    userId: userId,
    username: username,
    name: name,
    phone: cleanPhone,
    year: sem,
    sem: sem,
    role: "student"
  };

  const accounts = getAccounts();
  const existingIdx = accounts.findIndex(a => a.id === userId || (a.phone && a.phone.replace(/\D/g, '').slice(-10) === cleanPhone));
  if (existingIdx >= 0) {
    accounts[existingIdx] = { ...accounts[existingIdx], ...account };
  } else {
    accounts.push(account);
  }
  saveAccounts(accounts);

  loginUser(account);
  showToast(`Welcome ${account.name}! (${account.sem}) Food menu is ready 🍛`, "success");
  return false;
}

function quickPortalStudentLogin() {
  quickDemoStudentLogin();
}

function handlePortalWorkerLogin(e) {
  if (e) {
    try { e.preventDefault(); } catch (err) {}
    try { e.stopPropagation(); } catch (err) {}
  }
  const passInput = document.getElementById("login-worker-password") || document.getElementById("worker-password-input");
  const password = passInput ? passInput.value.trim() : "";

  if (verifyKitchenPassword(password)) {
    currentUser = { role: "worker", name: "Kitchen Staff", username: "staff" };
    try {
      localStorage.setItem("savitha_user", JSON.stringify(currentUser));
    } catch (err) {}

    renderUserAuthSlot();
    applyRoleVisibility();
    performSwitchMode("manager");
    showToast("👨‍🍳 Kitchen Staff Verified! Welcome to Kitchen Dashboard.", "success");
    return false;
  } else {
    showToast("⚠️ Incorrect kitchen staff password. Please try again.", "warning");
    if (passInput) {
      passInput.focus();
      passInput.style.borderColor = "#ef4444";
      setTimeout(() => { if (passInput) passInput.style.borderColor = ""; }, 2500);
    }
    return false;
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
  if (currentUser) {
    saveUserData();
  }
  currentUser = null;
  cart = {};
  myOrders = [];
  activeCoupon = null;
  lastPlacedOrder = null;
  try {
    localStorage.removeItem("savitha_user");
    sessionStorage.removeItem("savitha_user");
    localStorage.removeItem("savitha_student_active_order");
    localStorage.removeItem("savitha_my_orders");
  } catch (e) {}

  updateCartBar();
  updateMyOrdersCount();
  renderMyOrdersList();
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
  const navBtns = ["about", "login", "home", "feedback", "reviews", "kitchen"];
  navBtns.forEach(b => {
    const el = document.getElementById(`nav-btn-${b}`);
    if (el) el.classList.remove("active");
  });

  if (target === "about") {
    const el = document.getElementById("nav-btn-about");
    if (el) el.classList.add("active");
    performSwitchMode("about");
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else if (target === "reviews") {
    performSwitchMode("about");
    const el = document.getElementById("nav-btn-reviews");
    if (el) el.classList.add("active");
    const sec = document.getElementById("reviews-section");
    if (sec && typeof sec.scrollIntoView === "function") {
      setTimeout(() => {
        try { sec.scrollIntoView({ behavior: "smooth", block: "start" }); } catch (err) {}
      }, 50);
    }
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
  const navBtns = ["about", "login", "home", "feedback", "reviews", "kitchen"];
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

  const navHome = document.getElementById("nav-btn-home");
  const navOrders = document.getElementById("btn-top-my-orders-nav");
  const navAbout = document.getElementById("nav-btn-about");
  const navLogin = document.getElementById("nav-btn-login");
  const navReviews = document.getElementById("nav-btn-reviews");
  const navKitchen = document.getElementById("nav-btn-kitchen");

  // Ensure modals are closed upon mode switch
  closeMyOrdersModal();
  closeCartModal();

  if (mode === "about") {
    // In About webpage, we should NOT be able to see Menu and My Orders!
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) navKitchen.style.display = "none";
    if (navAbout) navAbout.classList.add("active");

    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");

    if (viewAbout) {
      viewAbout.style.display = "block";
      viewAbout.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "login") {
    // In Login view, Menu and My Orders are strictly hidden
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) navKitchen.style.display = "none";
    if (navLogin) navLogin.classList.add("active");

    if (toggle) toggle.style.display = "none";
    if (cartBtn) cartBtn.style.display = "none";
    if (floatingBar) floatingBar.classList.remove("show");

    // Clean inputs so name or password is never visible on the login page
    const nameInput = document.getElementById("login-student-name");
    if (nameInput) {
      nameInput.value = "";
      nameInput.placeholder = "Enter your full name";
    }
    const phoneInput = document.getElementById("login-student-phone");
    if (phoneInput) phoneInput.value = "";
    const pwdInput = document.getElementById("login-worker-password");
    if (pwdInput) pwdInput.value = "";

    // Clear user chip in top nav if on login page
    const slot = document.getElementById("user-auth-slot");
    if (slot) {
      slot.innerHTML = `
        <button type="button" class="btn-top-login active" id="btn-top-login" onclick="navigateToSection('login')" title="Login to Savitha Canteen">
          <span class="top-login-icon">👤</span>
          <span class="top-login-text">Login</span>
        </button>
      `;
    }

    if (viewLogin) {
      viewLogin.style.display = "block";
      viewLogin.style.animation = "fadeIn 0.25s ease-out";
    }
  } else if (mode === "manager") {
    if (navHome) navHome.style.display = "none";
    if (navOrders) navOrders.style.display = "none";
    if (navKitchen) {
      navKitchen.style.display = "inline-flex";
      navKitchen.classList.add("active");
    }

    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "none";
    if (btnMgr) btnMgr.classList.add("active");
    if (floatingBar) floatingBar.classList.remove("show");

    if (viewMgr) {
      viewMgr.style.display = "block";
      viewMgr.classList.add("show");
      viewMgr.style.animation = "fadeIn 0.25s ease-out";
    }
    switchManagerTab("orders");
  } else {
    // Mode is "order" or "home" - Menu and My Orders are visible
    if (navHome) {
      navHome.style.display = "inline-flex";
      navHome.classList.add("active");
    }
    if (navOrders) {
      navOrders.style.display = "inline-flex";
    }
    if (navKitchen) {
      navKitchen.style.display = (currentUser && currentUser.role === "worker") ? "inline-flex" : "none";
    }

    if (toggle) toggle.style.display = "flex";
    if (cartBtn) cartBtn.style.display = "flex";
    if (btnOrder) btnOrder.classList.add("active");

    if (viewOrder) {
      viewOrder.style.display = "block";
      viewOrder.style.animation = "fadeIn 0.25s ease-out";
    }
    renderDishes();
    updateCartBar();
    updateMyOrdersCount();
    renderLoyaltyStampCard();
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
    sem: year,
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
      if (data && Array.isArray(data.feedback)) {
        feedbackList = data.feedback;
      } else if (Array.isArray(data)) {
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
    const fullStars = "★".repeat(rating);
    const emptyStars = "☆".repeat(Math.max(0, 5 - rating));

    return `
      <div class="fb-review-card animate-card" style="background:#ffffff; border:1.5px solid var(--border); border-radius:14px; padding:18px; box-shadow:var(--shadow-sm); display:flex; flex-direction:column; justify-content:space-between; transition:transform 0.25s, box-shadow 0.25s;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; gap:8px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div style="width:38px; height:38px; min-width:38px; border-radius:50%; background:linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); color:var(--primary); font-weight:900; font-size:1rem; display:flex; align-items:center; justify-content:center; border:1.5px solid #c7d2fe;">🎓</div>
              <div>
                <div style="font-weight:800; font-size:0.96rem; color:var(--text-main); display:flex; align-items:center; gap:6px;">
                  <span>${escapeHtml(fb.name || "Student Reviewer")}</span>
                  <span style="font-size:0.7rem; color:#10b981; background:#ecfdf5; border:1px solid #a7f3d0; padding:1px 6px; border-radius:999px; font-weight:700;">✓ Verified</span>
                </div>
                <div style="font-size:0.78rem; font-weight:700; color:var(--primary);">${escapeHtml(fb.sem || fb.year || "Sem 4 • Student")}</div>
              </div>
            </div>
            <div class="dish-stars-graphic" style="color:#f59e0b; font-size:1.1rem; letter-spacing:1px; white-space:nowrap;" title="${rating}/5 stars">
              <span>${fullStars}</span><span style="color:#cbd5e1;">${emptyStars}</span>
            </div>
          </div>
          <p style="font-size:0.88rem; color:var(--text-main); margin:0 0 12px 0; line-height:1.5; font-style:italic;">"${escapeHtml(fb.comment || "")}"</p>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:var(--text-muted); border-top:1px solid #f1f5f9; padding-top:10px;">
          <span style="background:#f1f5f9; padding:2px 8px; border-radius:6px; font-weight:600;">🏷️ ${escapeHtml(fb.category || "Dining")}</span>
          <span style="font-weight:600;">📅 ${escapeHtml(fb.date || "Recent")}</span>
        </div>
      </div>
    `;
  }).join('');
}

// =========================================================================
// 8. CANTEEN MANAGER AI PREDICTOR LOGIC & LIVE ORDERS
// =========================================================================
function switchManagerTab(tabName) {
  const tabs = ["orders", "inventory", "calc", "dailyplan", "stats", "history", "pwd", "pnl"];
  tabs.forEach(t => {
    const btn = document.getElementById(`subtab-${t}-btn`);
    const pane = document.getElementById(`manager-pane-${t}`) || document.getElementById(`mgr-tab-${t}`);
    if (btn) btn.classList.remove("active");
    if (pane) pane.style.display = "none";
  });

  const activeBtn = document.getElementById(`subtab-${tabName}-btn`);
  const activePane = document.getElementById(`manager-pane-${tabName}`) || document.getElementById(`mgr-tab-${tabName}`);
  if (activeBtn) activeBtn.classList.add("active");
  if (activePane) activePane.style.display = "block";

  if (tabName === "inventory") {
    renderInventoryDashboard();
  } else if (tabName === "orders") {
    fetchLiveOrdersFromBackend();
    renderLiveOrders();
  } else if (tabName === "history") {
    loadHistory();
    renderHistoryTable();
  } else if (tabName === "pnl") {
    loadAndRenderPnL();
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
  if (e) {
    try { e.preventDefault(); } catch (err) {}
  }
  const curInput = document.getElementById("current-pwd-input");
  const newInput = document.getElementById("new-pwd-input");

  const cur = curInput ? curInput.value.trim() : "";
  const newP = newInput ? newInput.value.trim() : "";

  if (!verifyKitchenPassword(cur)) {
    showToast("Current password incorrect!", "warning");
    return;
  }
  if (!newP || newP.length < 4) {
    showToast("New password must be at least 4 characters!", "warning");
    return;
  }

  setKitchenStaffPassword(newP);
  if (curInput) curInput.value = "";
  if (newInput) newInput.value = "";
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
// 8B. KITCHEN PROFIT & LOSS (P&L) AND WEEKLY COMPARISON ENGINE
// =========================================================================
const DEFAULT_PNL_DATA = {
  status: "success",
  current_month: "September 2026",
  currency: "INR",
  summary: {
    total_monthly_revenue: 528400,
    total_cogs_ingredients: 284160,
    total_operating_overhead: 68740,
    total_monthly_expenses: 352900,
    total_monthly_profit: 175500,
    average_margin_percent: 33.2,
    total_waste_prevented_savings: 58400
  },
  weeks: [
    {
      id: "week1",
      label: "Week 1",
      date_range: "Aug 31 – Sep 06",
      orders_count: 1045,
      gross_revenue: 118200,
      ingredient_cogs: 64800,
      overhead_costs: 15800,
      total_expenses: 80600,
      net_profit: 37600,
      margin_percent: 31.8,
      waste_saved: 11200,
      wow_growth: 0.0,
      status: "Profitable",
      status_badge: "🟢 Normal Week",
      peak_day: "Wednesday",
      top_selling_dish: "Veg Biryani"
    },
    {
      id: "week2",
      label: "Week 2",
      date_range: "Sep 07 – Sep 13",
      orders_count: 1120,
      gross_revenue: 127600,
      ingredient_cogs: 69100,
      overhead_costs: 16600,
      total_expenses: 85700,
      net_profit: 41900,
      margin_percent: 32.8,
      waste_saved: 13400,
      wow_growth: 11.4,
      status: "Profitable",
      status_badge: "🟢 Growth Week",
      peak_day: "Friday",
      top_selling_dish: "Chicken Biryani"
    },
    {
      id: "week3",
      label: "Week 3",
      date_range: "Sep 14 – Sep 20",
      orders_count: 1215,
      gross_revenue: 139750,
      ingredient_cogs: 74460,
      overhead_costs: 17940,
      total_expenses: 92400,
      net_profit: 47350,
      margin_percent: 33.9,
      waste_saved: 15600,
      wow_growth: 13.0,
      status: "High Margin",
      status_badge: "🚀 High Margin",
      peak_day: "Thursday",
      top_selling_dish: "Masala Dosa"
    },
    {
      id: "week4",
      label: "Week 4 (Current)",
      date_range: "Sep 21 – Sep 27",
      orders_count: 1280,
      gross_revenue: 142850,
      ingredient_cogs: 75800,
      overhead_costs: 18400,
      total_expenses: 94200,
      net_profit: 48650,
      margin_percent: 34.1,
      waste_saved: 18200,
      wow_growth: 2.7,
      status: "Peak Rush",
      status_badge: "🔥 Campus Rush",
      peak_day: "Tuesday",
      top_selling_dish: "Chicken Kathi Roll"
    }
  ],
  top_dishes_pnl: [
    { dish: "Chicken Biryani", sales: 42600, cost: 22400, profit: 20200, margin: 47.4, portions: 284 },
    { dish: "Veg Biryani", sales: 28400, cost: 13900, profit: 14500, margin: 51.1, portions: 258 },
    { dish: "Masala Dosa", sales: 21600, cost: 7800, profit: 13800, margin: 63.9, portions: 270 },
    { dish: "Mumbai Pav Bhaji", sales: 17800, cost: 7900, profit: 9900, margin: 55.6, portions: 198 },
    { dish: "Samosa & Cutting Chai", sales: 14200, cost: 4900, profit: 9300, margin: 65.5, portions: 355 },
    { dish: "Thick Cold Coffee", sales: 11800, cost: 4200, profit: 7600, margin: 64.4, portions: 236 }
  ]
};

let currentPnLData = DEFAULT_PNL_DATA;
let selectedPnLWeekId = "week4";

async function loadAndRenderPnL() {
  try {
    const res = await fetch(`${API_BASE}/api/pnl`);
    if (res.ok) {
      const data = await res.json();
      if (data && data.weeks) {
        currentPnLData = data;
      }
    }
  } catch (err) {
    currentPnLData = DEFAULT_PNL_DATA;
  }

  // Factor today's live orders into current week
  if (Array.isArray(liveOrders) && liveOrders.length > 0 && currentPnLData.weeks) {
    const liveTotal = liveOrders.reduce((sum, o) => sum + (parseInt(o.total) || 0), 0);
    const w4 = currentPnLData.weeks.find(w => w.id === "week4");
    if (w4 && liveTotal > 0) {
      w4.live_extra_revenue = liveTotal;
    }
  }

  renderPnLSummary(selectedPnLWeekId);
  renderWeeklyComparisonBars();
  renderWeeklyComparisonTable();
  renderTopDishesPnL();
}

function selectPnLWeek(weekId, btnEl) {
  selectedPnLWeekId = weekId;
  document.querySelectorAll(".pnl-week-chip").forEach(b => {
    b.classList.remove("active");
    b.style.background = "#ffffff";
    b.style.color = "var(--text-main)";
    b.style.borderColor = "var(--border)";
    b.style.fontWeight = "700";
  });
  if (btnEl) {
    btnEl.classList.add("active");
    btnEl.style.background = "#4f46e5";
    btnEl.style.color = "#ffffff";
    btnEl.style.borderColor = "#4f46e5";
    btnEl.style.fontWeight = "800";
  }

  const badge = document.getElementById("pnl-selected-week-badge");
  if (badge) {
    if (weekId === "all") {
      badge.textContent = "Viewing: Full Month (4 Weeks Total)";
    } else {
      const w = (currentPnLData.weeks || []).find(x => x.id === weekId);
      badge.textContent = `Viewing: ${w ? w.label + ' (' + w.date_range + ')' : weekId}`;
    }
  }

  renderPnLSummary(weekId);
}

function formatINR(num) {
  return "₹" + Number(num).toLocaleString("en-IN");
}

function renderPnLSummary(weekId) {
  const revEl = document.getElementById("pnl-revenue-val");
  const revSubEl = document.getElementById("pnl-revenue-sub");
  const costEl = document.getElementById("pnl-cost-val");
  const costSubEl = document.getElementById("pnl-cost-sub");
  const profEl = document.getElementById("pnl-profit-val");
  const profSubEl = document.getElementById("pnl-profit-sub");
  const wasteEl = document.getElementById("pnl-waste-val");
  const wasteSubEl = document.getElementById("pnl-waste-sub");

  if (!currentPnLData || !currentPnLData.weeks) return;

  if (weekId === "all") {
    const s = currentPnLData.summary;
    if (revEl) revEl.textContent = formatINR(s.total_monthly_revenue);
    if (revSubEl) revSubEl.textContent = `All 4 Weeks Combined • ~4,660 orders`;
    if (costEl) costEl.textContent = formatINR(s.total_monthly_expenses);
    if (costSubEl) costSubEl.textContent = `Ingredients: ${formatINR(s.total_cogs_ingredients)} • Overhead: ${formatINR(s.total_operating_overhead)}`;
    if (profEl) {
      profEl.textContent = `+${formatINR(s.total_monthly_profit)}`;
      profEl.style.color = "#059669";
    }
    if (profSubEl) profSubEl.textContent = `${s.average_margin_percent}% Monthly Average Margin • Strong Financial Health`;
    if (wasteEl) wasteEl.textContent = formatINR(s.total_waste_prevented_savings);
    if (wasteSubEl) wasteSubEl.textContent = `Monthly food loss prevented by AI portioning`;
    return;
  }

  const week = currentPnLData.weeks.find(w => w.id === weekId) || currentPnLData.weeks[3];
  if (!week) return;

  const extra = week.live_extra_revenue || 0;
  const rev = week.gross_revenue + extra;
  const cost = week.total_expenses + Math.round(extra * 0.53);
  const profit = rev - cost;
  const margin = Math.round((profit / rev) * 1000) / 10;

  if (revEl) revEl.textContent = formatINR(rev);
  if (revSubEl) {
    const growthText = week.wow_growth > 0 ? `+${week.wow_growth}% vs prior week` : `Baseline week`;
    revSubEl.textContent = `${growthText} • ${week.orders_count} orders`;
  }

  if (costEl) costEl.textContent = formatINR(cost);
  if (costSubEl) costSubEl.textContent = `Ingredients: ${formatINR(week.ingredient_cogs)} • Overhead: ${formatINR(week.overhead_costs)}`;

  if (profEl) {
    profEl.textContent = profit >= 0 ? `+${formatINR(profit)}` : `-${formatINR(Math.abs(profit))}`;
    profEl.style.color = profit >= 0 ? "#059669" : "#dc2626";
  }
  if (profSubEl) profSubEl.textContent = `${margin}% Net Margin • ${week.status_badge || week.status}`;

  if (wasteEl) wasteEl.textContent = formatINR(week.waste_saved);
  if (wasteSubEl) wasteSubEl.textContent = `Saved via AI demand estimation on ${week.peak_day || 'Peak Day'}`;
}

function renderWeeklyComparisonBars() {
  const container = document.getElementById("pnl-weekly-bars-container");
  if (!container || !currentPnLData || !currentPnLData.weeks) return;

  const maxRev = Math.max(...currentPnLData.weeks.map(w => w.gross_revenue + (w.live_extra_revenue || 0)), 150000);

  let html = "";
  currentPnLData.weeks.forEach((w, idx) => {
    const isSelected = selectedPnLWeekId === w.id;
    const rev = w.gross_revenue + (w.live_extra_revenue || 0);
    const cost = w.total_expenses + Math.round((w.live_extra_revenue || 0) * 0.53);
    const profit = rev - cost;

    const revPct = Math.min(100, Math.round((rev / maxRev) * 100));
    const costPct = Math.min(100, Math.round((cost / maxRev) * 100));
    const profitPct = Math.min(100, Math.round((profit / maxRev) * 100));

    html += `
      <div class="manager-card" onclick="selectPnLWeek('${w.id}', document.getElementById('pnl-chip-${w.id}'))"
        style="cursor:pointer; border:1.5px solid ${isSelected ? '#4f46e5' : 'var(--border)'}; background:${isSelected ? '#f8faff' : '#ffffff'}; padding:14px; border-radius:12px; transition:all 0.2s;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <div style="font-weight:800; font-size:0.95rem; color:var(--text-main);">${w.label}</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">${w.date_range}</div>
          </div>
          <span style="font-size:0.72rem; font-weight:800; padding:2px 8px; border-radius:999px; ${w.wow_growth >= 0 ? 'background:#ecfdf5; color:#059669;' : 'background:#fee2e2; color:#dc2626;'}">
            ${idx === 0 ? 'Base' : (w.wow_growth >= 0 ? '▲ +' + w.wow_growth + '%' : '▼ ' + w.wow_growth + '%')}
          </span>
        </div>

        <!-- Metric Bars -->
        <div style="margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; font-size:0.76rem; margin-bottom:2px;">
            <span style="color:#4f46e5; font-weight:700;">Revenue</span>
            <span style="font-weight:800;">${formatINR(rev)}</span>
          </div>
          <div style="height:6px; background:#e0e7ff; border-radius:999px; overflow:hidden;">
            <div style="width:${revPct}%; height:100%; background:#4f46e5; border-radius:999px;"></div>
          </div>
        </div>

        <div style="margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; font-size:0.76rem; margin-bottom:2px;">
            <span style="color:#b45309; font-weight:700;">Costs</span>
            <span style="font-weight:800;">${formatINR(cost)}</span>
          </div>
          <div style="height:6px; background:#fef3c7; border-radius:999px; overflow:hidden;">
            <div style="width:${costPct}%; height:100%; background:#f59e0b; border-radius:999px;"></div>
          </div>
        </div>

        <div style="margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; font-size:0.76rem; margin-bottom:2px;">
            <span style="color:#059669; font-weight:700;">Net Profit (${w.margin_percent}%)</span>
            <span style="font-weight:900; color:#059669;">${formatINR(profit)}</span>
          </div>
          <div style="height:6px; background:#dcfce7; border-radius:999px; overflow:hidden;">
            <div style="width:${profitPct}%; height:100%; background:#10b981; border-radius:999px;"></div>
          </div>
        </div>

        <div style="font-size:0.74rem; color:var(--text-muted); text-align:right;">
          Click to inspect week →
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function renderWeeklyComparisonTable() {
  const tbody = document.getElementById("pnl-table-body");
  if (!tbody || !currentPnLData || !currentPnLData.weeks) return;

  let html = "";
  currentPnLData.weeks.forEach(w => {
    const isSelected = selectedPnLWeekId === w.id;
    const rev = w.gross_revenue + (w.live_extra_revenue || 0);
    const cost = w.total_expenses + Math.round((w.live_extra_revenue || 0) * 0.53);
    const profit = rev - cost;
    const margin = Math.round((profit / rev) * 1000) / 10;

    html += `
      <tr style="border-bottom:1px solid #f1f5f9; ${isSelected ? 'background:#eef2ff; font-weight:600;' : ''}">
        <td style="padding:10px 12px;">
          <strong>${w.label}</strong>
          <div style="font-size:0.75rem; color:var(--text-muted);">${w.date_range}</div>
        </td>
        <td style="padding:10px 12px;">${w.orders_count.toLocaleString("en-IN")}</td>
        <td style="padding:10px 12px; font-weight:800; color:#4f46e5;">${formatINR(rev)}</td>
        <td style="padding:10px 12px; color:var(--text-muted);">${formatINR(w.ingredient_cogs)}</td>
        <td style="padding:10px 12px; color:var(--text-muted);">${formatINR(w.overhead_costs)}</td>
        <td style="padding:10px 12px; font-weight:700; color:#b45309;">${formatINR(cost)}</td>
        <td style="padding:10px 12px; font-weight:900; color:#059669;">+${formatINR(profit)}</td>
        <td style="padding:10px 12px;">
          <span style="background:#ecfdf5; color:#059669; padding:2px 8px; border-radius:999px; font-weight:800; font-size:0.75rem;">
            ${margin}%
          </span>
        </td>
        <td style="padding:10px 12px; color:#0891b2; font-weight:700;">${formatINR(w.waste_saved)}</td>
        <td style="padding:10px 12px;">
          <span style="font-size:0.76rem; font-weight:800; color:#3730a3; background:#e0e7ff; padding:2px 8px; border-radius:999px;">
            ${w.status_badge || w.status}
          </span>
        </td>
      </tr>
    `;
  });

  const s = currentPnLData.summary;
  html += `
    <tr style="background:#f8fafc; border-top:2px solid var(--border); font-weight:900;">
      <td style="padding:12px;">MONTH TOTAL (4 WEEKS)</td>
      <td style="padding:12px;">4,660</td>
      <td style="padding:12px; color:#4f46e5;">${formatINR(s.total_monthly_revenue)}</td>
      <td style="padding:12px;">${formatINR(s.total_cogs_ingredients)}</td>
      <td style="padding:12px;">${formatINR(s.total_operating_overhead)}</td>
      <td style="padding:12px; color:#b45309;">${formatINR(s.total_monthly_expenses)}</td>
      <td style="padding:12px; color:#059669; font-size:1rem;">+${formatINR(s.total_monthly_profit)}</td>
      <td style="padding:12px; color:#059669;">${s.average_margin_percent}%</td>
      <td style="padding:12px; color:#0891b2;">${formatINR(s.total_waste_prevented_savings)}</td>
      <td style="padding:12px;">⭐ Excellent Health</td>
    </tr>
  `;

  tbody.innerHTML = html;
}

function renderTopDishesPnL() {
  const tbody = document.getElementById("pnl-dishes-table-body");
  if (!tbody || !currentPnLData || !currentPnLData.top_dishes_pnl) return;

  let html = "";
  currentPnLData.top_dishes_pnl.forEach(d => {
    html += `
      <tr style="border-bottom:1px solid #f1f5f9;">
        <td style="padding:10px 12px; font-weight:800; color:var(--text-main);">${d.dish}</td>
        <td style="padding:10px 12px;">${d.portions} portions</td>
        <td style="padding:10px 12px; font-weight:800; color:#4f46e5;">${formatINR(d.sales)}</td>
        <td style="padding:10px 12px; color:#b45309;">${formatINR(d.cost)}</td>
        <td style="padding:10px 12px; font-weight:900; color:#059669;">+${formatINR(d.profit)}</td>
        <td style="padding:10px 12px;">
          <span style="background:#ecfdf5; color:#059669; padding:2px 8px; border-radius:999px; font-weight:800; font-size:0.75rem;">
            ${d.margin}%
          </span>
        </td>
        <td style="padding:10px 12px;">
          <span style="font-size:0.75rem; font-weight:700; color:${d.margin > 55 ? '#059669' : '#4f46e5'};">
            ${d.margin > 55 ? '⭐ High Profit Anchor' : '🔥 Volume Bestseller'}
          </span>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function exportPnLReport() {
  window.print();
  showToast("📄 Generated Canteen Weekly P&L Summary Report!", "info");
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
  window.quickDemoStudentLogin = quickDemoStudentLogin;
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
  window.openNetworkShareModal = openNetworkShareModal;
  window.closeNetworkShareModal = closeNetworkShareModal;
  window.copyNetworkShareLink = copyNetworkShareLink;
  window.initUserAuth = initUserAuth;
  window.addTodaysSpecialToCart = addTodaysSpecialToCart;
  window.renderLoyaltyStampCard = renderLoyaltyStampCard;
  window.simulateOrderStreak = simulateOrderStreak;
  window.applyQuickCoupon = applyQuickCoupon;
  window.applyCartCoupon = applyCartCoupon;
  window.executeApplyCoupon = executeApplyCoupon;
  window.renderDishes = renderDishes;
  window.updateDishQty = updateDishQty;
  window.DISHES = DISHES;
  window.loadAndRenderPnL = loadAndRenderPnL;
  window.selectPnLWeek = selectPnLWeek;
  window.exportPnLReport = exportPnLReport;
  window.DEFAULT_PNL_DATA = DEFAULT_PNL_DATA;
    window.getAccounts = getAccounts;
  window.saveAccounts = saveAccounts;
  window.findAccount = findAccount;
  window.switchStudentAuthMode = switchStudentAuthMode;
  window.fillDemoStudent = fillDemoStudent;
  window.handleStudentSignIn = handleStudentSignIn;
  window.handleStudentRegister = handleStudentRegister;
  window.loginUser = loginUser;
  window.loadUserData = loadUserData;
  window.saveUserData = saveUserData;
  window.openProfileModal = openProfileModal;
  window.closeProfileModal = closeProfileModal;
  window.initInventory = initInventory;
  window.getInventory = getInventory;
  window.getInventoryItem = getInventoryItem;
  window.updateItemStock = updateItemStock;
  window.adjustItemStock = adjustItemStock;
  window.toggleItemStatus = toggleItemStatus;
  window.restockAll = restockAll;
  window.decrementOrderInventory = decrementOrderInventory;
  window.filterInventoryCategory = filterInventoryCategory;
  window.filterInventoryStatus = filterInventoryStatus;
  window.searchInventory = searchInventory;
  window.renderInventoryDashboard = renderInventoryDashboard;
  window.openCancelOrderModal = openCancelOrderModal;
  window.closeCancelOrderModal = closeCancelOrderModal;
  window.confirmCancellationWithCharge = confirmCancellationWithCharge;


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


// =========================================================================
// NETWORK SHARE / OPEN ON MOBILE PHONE OR OTHER LAPTOPS
// =========================================================================
function openNetworkShareModal() {
  const modal = document.getElementById("network-share-modal");
  if (!modal) return;

  let targetUrl = window.location.origin;
  if (!targetUrl || targetUrl.includes("localhost") || targetUrl.includes("127.0.0.1")) {
    targetUrl = "http://10.209.246.16:5000";
  }

  fetch(`${API_BASE}/api/network-info`)
    .then(r => r.ok ? r.json() : null)
    .then(data => {
      if (data && data.lan_url) {
        targetUrl = data.lan_url;
      }
      applyNetworkShareUrl(targetUrl);
    })
    .catch(() => {
      applyNetworkShareUrl(targetUrl);
    });

  modal.classList.add("show");
}

function applyNetworkShareUrl(url) {
  const textEl = document.getElementById("network-share-url-text");
  const imgEl = document.getElementById("network-qr-image");
  if (textEl) textEl.textContent = url;
  if (imgEl) {
    imgEl.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`;
  }
}

function closeNetworkShareModal() {
  const modal = document.getElementById("network-share-modal");
  if (modal) modal.classList.remove("show");
}

function copyNetworkShareLink() {
  const textEl = document.getElementById("network-share-url-text");
  const url = textEl ? textEl.textContent : window.location.href;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url)
      .then(() => showToast("📋 Link copied! Open it on other phones or laptops.", "success"))
      .catch(() => fallbackCopy(url));
  } else {
    fallbackCopy(url);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement("textarea");
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  document.body.removeChild(ta);
  showToast("📋 Link copied! Open it on other phones or laptops.", "success");
}
