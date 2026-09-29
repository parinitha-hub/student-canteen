import sys

NEW_DISHES_CODE = '''const DISHES = [
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
    desc: "Creamy iced blended coffee crafted with rich roasted espresso, chilled milk, and a decadent drizzle of Hershey\\'s chocolate syrup.",
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
  }
];'''

with open('scratch/build_clean_app_js.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace DISHES block
start_idx = content.find('const DISHES = [')
end_idx = content.find('];', start_idx) + 2

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + NEW_DISHES_CODE + content[end_idx:]
    print("Replaced DISHES block in scratch/build_clean_app_js.py")
else:
    print("Could not find DISHES block")
    sys.exit(1)

# Ensure selectKitchenDish is added
if 'function selectKitchenDish' not in content:
    calc_func_idx = content.find('function selectDishForKitchenCalc')
    select_kitchen_dish_code = '''function selectKitchenDish(dishName, el) {
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

'''
    content = content[:calc_func_idx] + select_kitchen_dish_code + content[calc_func_idx:]
    # And export on window
    window_idx = content.find('window.selectDishForKitchenCalc = selectDishForKitchenCalc;')
    content = content[:window_idx] + 'window.selectKitchenDish = selectKitchenDish;\n  ' + content[window_idx:]
    print("Added selectKitchenDish function and window export")

with open('scratch/build_clean_app_js.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated scratch/build_clean_app_js.py successfully!")
