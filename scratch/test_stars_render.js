const fs = require('fs');
const appCode = fs.readFileSync('js/app.js', 'utf-8');
const element = { innerHTML: '' };
global.document = {
  getElementById: (id) => id === 'dishes-grid' ? element : { classList: { remove: ()=>{} } },
  querySelectorAll: () => []
};
global.cart = {};
global.currentCategory = 'all';
eval(appCode);
renderDishes();
console.log('Dishes rendered, length:', element.innerHTML.length);
console.log('Contains stars graphic:', element.innerHTML.includes('dish-stars-graphic'));
const match = element.innerHTML.match(/<div class="dish-star-rating-row"[\s\S]*?<\/div>/);
if (match) {
  console.log('Sample dish star rating HTML:');
  console.log(match[0]);
}
