const fs = require('fs');

console.log("Testing reviews loading and rendering...");
const reviewsGrid = {
  id: "reviews-cards-grid",
  innerHTML: ""
};

global.document = {
  getElementById: (id) => {
    if (id === "reviews-cards-grid") return reviewsGrid;
    return { style: {}, classList: { add: ()=>{}, remove: ()=>{} }, appendChild: ()=>{}, remove: ()=>{} };
  },
  querySelectorAll: () => []
};

global.window = {
  scrollTo: () => {},
  location: { origin: "http://127.0.0.1:5000" }
};

global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

global.sessionStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

// Evaluate app.js
const appCode = fs.readFileSync('js/app.js', 'utf-8');
eval(appCode);

// Test loadFeedback with fallback
loadFeedback().then(() => {
  console.log("Reviews grid HTML length:", reviewsGrid.innerHTML.length);
  console.log("Reviews contains star rating:", reviewsGrid.innerHTML.includes("★"));
  console.log("Reviews contains verified dining:", reviewsGrid.innerHTML.includes("Verified Dining"));
  if (reviewsGrid.innerHTML.length > 200) {
    console.log("✓ Reviews loaded and rendered successfully!");
    process.exit(0);
  } else {
    console.error("✗ Reviews failed to render");
    process.exit(1);
  }
}).catch(err => {
  console.error("Error testing feedback:", err);
  process.exit(1);
});
