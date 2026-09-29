const fs = require('fs');
const http = require('http');

console.log("=================================================");
console.log("🧪 TESTING KITCHEN STAFF PROFIT & LOSS (P&L)");
console.log("=================================================");

// Step 1: Test Backend /api/pnl Endpoint
function testBackendPnLEndpoint() {
  return new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:5000/api/pnl', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.status === "success" && Array.isArray(json.weeks) && json.weeks.length === 4) {
            console.log("✓ Backend /api/pnl responded successfully with 4 audited weeks!");
            console.log(`  - Month: ${json.current_month}`);
            console.log(`  - Total Revenue: ₹${json.summary.total_monthly_revenue.toLocaleString('en-IN')}`);
            console.log(`  - Total Profit: ₹${json.summary.total_monthly_profit.toLocaleString('en-IN')} (${json.summary.average_margin_percent}% margin)`);
            console.log(`  - AI Waste Prevented: ₹${json.summary.total_waste_prevented_savings.toLocaleString('en-IN')}`);
            resolve(json);
          } else {
            reject(new Error("Invalid P&L data format from backend"));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', (err) => {
      console.warn("Notice: Backend server not reachable via http in this step, testing frontend with default P&L dataset:", err.message);
      resolve(null);
    });
  });
}

// Step 2: Test Frontend P&L Logic in Mocked DOM
async function testFrontendPnL() {
  const elements = {};
  function createElementMock(id, tag = 'div') {
    return {
      id: id,
      tagName: tag.toUpperCase(),
      style: {},
      classList: {
        _classes: new Set(),
        add: function(c) { this._classes.add(c); },
        remove: function(c) { this._classes.delete(c); },
        contains: function(c) { return this._classes.has(c); }
      },
      value: '',
      textContent: '',
      innerHTML: '',
      children: [],
      appendChild: function(c) { this.children.push(c); },
      removeChild: function(c) { this.children = this.children.filter(x => x !== c); },
      remove: function() {},
      addEventListener: () => {},
      focus: () => {}
    };
  }

  const mockIds = [
    "nav-btn-kitchen", "view-manager", "view-about", "view-login", "view-order",
    "subtab-orders-btn", "subtab-calc-btn", "subtab-pnl-btn", "subtab-pwd-btn",
    "manager-pane-orders", "manager-pane-calc", "manager-pane-pnl", "manager-pane-pwd",
    "pnl-chip-week4", "pnl-chip-week3", "pnl-chip-week2", "pnl-chip-week1", "pnl-chip-all",
    "pnl-selected-week-badge", "pnl-revenue-val", "pnl-revenue-sub",
    "pnl-cost-val", "pnl-cost-sub", "pnl-profit-val", "pnl-profit-sub",
    "pnl-waste-val", "pnl-waste-sub", "pnl-weekly-bars-container",
    "pnl-table-body", "pnl-dishes-table-body", "toast-container"
  ];

  mockIds.forEach(id => {
    elements[id] = createElementMock(id);
  });

  global.document = {
    getElementById: (id) => elements[id] || createElementMock(id),
    querySelectorAll: (sel) => {
      if (sel === ".pnl-week-chip") {
        return [elements["pnl-chip-week4"], elements["pnl-chip-week3"], elements["pnl-chip-week2"], elements["pnl-chip-week1"], elements["pnl-chip-all"]];
      }
      return [];
    },
    createElement: (tag) => createElementMock('dynamic', tag),
    documentElement: { setAttribute: () => {}, removeAttribute: () => {} }
  };

  global.window = {
    scrollTo: () => {},
    location: { origin: "http://127.0.0.1:5000" },
    confirm: () => true,
    print: () => {}
  };

  global.localStorage = {
    _store: {},
    getItem: function(k) { return this._store[k] || null; },
    setItem: function(k, v) { this._store[k] = String(v); },
    removeItem: function(k) { delete this._store[k]; }
  };

  global.sessionStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };

  // Load app.js
  const appCode = fs.readFileSync('js/app.js', 'utf-8');
  eval(appCode);

  console.log("\n--- TEST: Kitchen Subtab Switching to P&L ---");
  switchManagerTab('pnl');

  const pnlPane = elements["manager-pane-pnl"];
  const ordersPane = elements["manager-pane-orders"];
  const calcPane = elements["manager-pane-calc"];
  const pwdPane = elements["manager-pane-pwd"];

  console.log("P&L Pane display:", pnlPane.style.display, "(Expected: block)");
  console.log("Orders Pane display:", ordersPane.style.display, "(Expected: none)");
  console.log("Calc Pane display:", calcPane.style.display, "(Expected: none)");
  console.log("Staff Password Pane display:", pwdPane.style.display, "(Expected: none)");

  if (pnlPane.style.display !== "block" || ordersPane.style.display !== "none") {
    throw new Error("switchManagerTab('pnl') failed to display manager-pane-pnl");
  }
  console.log("✓ Subtab switched to Profit & Loss dashboard successfully!");

  console.log("\n--- TEST: P&L Data Loading and Rendering ---");
  await loadAndRenderPnL();

  console.log("Revenue displayed:", elements["pnl-revenue-val"].textContent);
  console.log("Costs displayed:", elements["pnl-cost-val"].textContent);
  console.log("Profit displayed:", elements["pnl-profit-val"].textContent);
  console.log("AI Waste Saved displayed:", elements["pnl-waste-val"].textContent);

  if (!elements["pnl-revenue-val"].textContent.includes("₹") || !elements["pnl-profit-val"].textContent.includes("₹")) {
    throw new Error("P&L metric cards failed to format in INR");
  }
  console.log("✓ P&L metric cards rendered in INR with high fidelity!");

  console.log("\n--- TEST: Week-over-Week Selection & Filtering ---");
  // Select Week 1
  selectPnLWeek('week1', elements["pnl-chip-week1"]);
  console.log("Week 1 Revenue:", elements["pnl-revenue-val"].textContent, "(Expected: ₹1,18,200)");
  console.log("Week 1 Profit:", elements["pnl-profit-val"].textContent, "(Expected: +₹37,600)");
  if (elements["pnl-revenue-val"].textContent !== "₹1,18,200" || elements["pnl-profit-val"].textContent !== "+₹37,600") {
    throw new Error("Week 1 metric values do not match expected audited amounts");
  }
  console.log("✓ Week 1 selection displays correct revenue and profit!");

  // Select Week 3
  selectPnLWeek('week3', elements["pnl-chip-week3"]);
  console.log("Week 3 Revenue:", elements["pnl-revenue-val"].textContent, "(Expected: ₹1,39,750)");
  console.log("Week 3 Profit:", elements["pnl-profit-val"].textContent, "(Expected: +₹47,350)");
  if (elements["pnl-revenue-val"].textContent !== "₹1,39,750" || elements["pnl-profit-val"].textContent !== "+₹47,350") {
    throw new Error("Week 3 metric values do not match expected audited amounts");
  }
  console.log("✓ Week 3 selection displays correct revenue and profit!");

  // Select Full Month
  selectPnLWeek('all', elements["pnl-chip-all"]);
  console.log("Month Total Revenue:", elements["pnl-revenue-val"].textContent, "(Expected: ₹5,28,400)");
  console.log("Month Total Profit:", elements["pnl-profit-val"].textContent, "(Expected: +₹1,75,500)");
  if (elements["pnl-revenue-val"].textContent !== "₹5,28,400" || elements["pnl-profit-val"].textContent !== "+₹1,75,500") {
    throw new Error("Full Month total metric values do not match expected audited amounts");
  }
  console.log("✓ Full month overview displays aggregated monthly total revenue and profit!");

  console.log("\n--- TEST: Weekly Comparison Bars & Table ---");
  const barsHtml = elements["pnl-weekly-bars-container"].innerHTML;
  const tableHtml = elements["pnl-table-body"].innerHTML;
  const dishesHtml = elements["pnl-dishes-table-body"].innerHTML;

  if (!barsHtml.includes("Week 1") || !barsHtml.includes("Week 4")) {
    throw new Error("Weekly comparison bar container is missing week data");
  }
  console.log("✓ Weekly comparison bar cards generated for all weeks!");

  if (!tableHtml.includes("MONTH TOTAL (4 WEEKS)") || !tableHtml.includes("Aug 31")) {
    throw new Error("Weekly comparison financial ledger table missing rows");
  }
  console.log("✓ Week-over-Week financial ledger table populated!");

  if (!dishesHtml.includes("Chicken Biryani") || !dishesHtml.includes("Masala Dosa")) {
    throw new Error("Dish profitability breakdown table missing items");
  }
  console.log("✓ Dish-level profitability & margins breakdown table populated!");

  console.log("\n=================================================");
  console.log("🎉 ALL KITCHEN PROFIT & LOSS TESTS PASSED 100%!");
  console.log("=================================================");
}

async function run() {
  try {
    await testBackendPnLEndpoint();
    await testFrontendPnL();
  } catch (err) {
    console.error("Test failed:", err);
    process.exit(1);
  }
}

run();
