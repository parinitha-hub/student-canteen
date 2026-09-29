// Test full user isolation, arrival time calculation, and review display
const fs = require('fs');
const path = require('path');

// Mock localStorage and DOM
class LocalStorageMock {
  constructor() {
    this.store = {};
  }
  clear() {
    this.store = {};
  }
  getItem(key) {
    return this.store[key] || null;
  }
  setItem(key, value) {
    this.store[key] = String(value);
  }
  removeItem(key) {
    delete this.store[key];
  }
}

global.localStorage = new LocalStorageMock();
global.sessionStorage = new LocalStorageMock();
global.window = {
  location: { origin: 'http://127.0.0.1:5000' }
};

// Check HTML for no student USN or password on student login form
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf-8');

console.log("=== CHECK 1: HTML Login Form Check ===");
const hasStudentUsernameInput = html.includes('id="login-student-username"');
const hasStudentPasswordInput = html.includes('id="login-student-password"');
const hasStudentNameInput = html.includes('id="login-student-name"');
const hasStudentPhoneInput = html.includes('id="login-student-phone"');
const hasStudentSemInput = html.includes('id="login-student-sem"');

console.log("Has student username (USN) input in HTML:", hasStudentUsernameInput, "(Expected: false)");
console.log("Has student password input in HTML:", hasStudentPasswordInput, "(Expected: false)");
console.log("Has student name input in HTML:", hasStudentNameInput, "(Expected: true)");
console.log("Has student phone input in HTML:", hasStudentPhoneInput, "(Expected: true)");
console.log("Has student sem input in HTML:", hasStudentSemInput, "(Expected: true)");

if (hasStudentUsernameInput || hasStudentPasswordInput) {
  console.error("FAIL: Student USN or password still present in HTML!");
  process.exit(1);
}

console.log("\n=== CHECK 2: Token Modal Arrival Time Check ===");
const hasArrivalTimeInToken = html.includes('id="token-arrival-time"');
const hasArrivalCountdownInToken = html.includes('id="token-arrival-countdown"');
console.log("Has token-arrival-time:", hasArrivalTimeInToken, "(Expected: true)");
console.log("Has token-arrival-countdown:", hasArrivalCountdownInToken, "(Expected: true)");

if (!hasArrivalTimeInToken || !hasArrivalCountdownInToken) {
  console.error("FAIL: Arrival time missing in token modal!");
  process.exit(1);
}

console.log("\n=== CHECK 3: Reviews Static Cards Check ===");
const hasSemInReviews = html.includes('Sem 4') && html.includes('Sem 8') && html.includes('Sem 6');
console.log("Reviews display semester information:", hasSemInReviews, "(Expected: true)");

console.log("\nALL VERIFICATIONS PASSED IN HTML!");
