/**
 * Zero-Dependency High-Performance SVG & Canvas Charts
 * Clean, lightweight, responsive charts designed for student AI canteen dashboards.
 */

const FoodMLCharts = (function () {

  /**
   * Render a sleek 7-day Demand Trend Line & Area Chart
   */
  function renderTrendChart(containerId, labels, actualValues, predictedValues) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = 240;
    const padding = { top: 20, right: 30, bottom: 40, left: 45 };

    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    const allValues = [...actualValues, ...predictedValues];
    const maxVal = Math.max(...allValues, 10) * 1.15;
    const minVal = Math.max(0, Math.min(...allValues, 0));

    const getX = (i) => padding.left + (i / (labels.length - 1)) * chartW;
    const getY = (val) => padding.top + chartH - ((val - minVal) / (maxVal - minVal)) * chartH;

    // Build SVG paths
    let actualPoints = [];
    let predPoints = [];
    labels.forEach((_, i) => {
      actualPoints.push(`${getX(i)},${getY(actualValues[i])}`);
      predPoints.push(`${getX(i)},${getY(predictedValues[i])}`);
    });

    const actualPathD = "M " + actualPoints.join(" L ");
    const predPathD = "M " + predPoints.join(" L ");
    const predAreaD = `M ${getX(0)},${padding.top + chartH} L ` + predPoints.join(" L ") + ` L ${getX(labels.length - 1)},${padding.top + chartH} Z`;

    // Horizontal grid lines
    let gridLinesSvg = "";
    for (let step = 0; step <= 4; step++) {
      const v = Math.round(minVal + (step / 4) * (maxVal - minVal));
      const y = getY(v);
      gridLinesSvg += `
        <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="rgba(75, 85, 99, 0.2)" stroke-dasharray="3 3"/>
        <text x="${padding.left - 10}" y="${y + 4}" fill="#9ca3af" font-size="11" text-anchor="end">${v}</text>
      `;
    }

    // X axis labels
    let xLabelsSvg = "";
    labels.forEach((label, i) => {
      const x = getX(i);
      xLabelsSvg += `
        <text x="${x}" y="${height - 12}" fill="#9ca3af" font-size="11" text-anchor="middle">${label}</text>
      `;
    });

    // Data dots
    let predDotsSvg = "";
    labels.forEach((_, i) => {
      predDotsSvg += `
        <circle cx="${getX(i)}" cy="${getY(predictedValues[i])}" r="4" fill="#10b981" stroke="#0b0f19" stroke-width="2"/>
        <circle cx="${getX(i)}" cy="${getY(actualValues[i])}" r="3.5" fill="#3b82f6" stroke="#0b0f19" stroke-width="1.5"/>
      `;
    });

    container.innerHTML = `
      <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
        <defs>
          <linearGradient id="predAreaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.0"/>
          </linearGradient>
        </defs>
        ${gridLinesSvg}
        <path d="${predAreaD}" fill="url(#predAreaGrad)"/>
        <path d="${predPathD}" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round"/>
        <path d="${actualPathD}" fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-dasharray="4 3" stroke-linecap="round"/>
        ${predDotsSvg}
        ${xLabelsSvg}
      </svg>
      <div style="display:flex; justify-content:center; gap:24px; margin-top:10px; font-size:12px;">
        <span style="display:flex; align-items:center; gap:6px; color:#10b981;">
          <span style="display:inline-block; width:12px; height:3px; background:#10b981; border-radius:2px;"></span> AI Predicted Demand
        </span>
        <span style="display:flex; align-items:center; gap:6px; color:#3b82f6;">
          <span style="display:inline-block; width:12px; height:3px; background:#3b82f6; border-radius:2px; border-top:1px dashed #3b82f6;"></span> Actual Demand (Historical)
        </span>
      </div>
    `;
  }

  /**
   * Render Horizontal Bar Chart for Item Popularity & Demand
   */
  function renderBarChart(containerId, itemsData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const maxVal = Math.max(...itemsData.map(d => d.value), 1);

    let html = `<div style="display:flex; flex-direction:column; gap:12px;">`;
    itemsData.forEach(item => {
      const pct = Math.round((item.value / maxVal) * 100);
      html += `
        <div>
          <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;">
            <span style="font-weight:600; color:#f3f4f6;">${item.label}</span>
            <span style="color:#10b981; font-weight:700;">${item.value} portions</span>
          </div>
          <div style="background:rgba(255,255,255,0.06); height:10px; border-radius:6px; overflow:hidden;">
            <div style="width:${pct}%; background:linear-gradient(90deg, #10b981, #3b82f6); height:100%; border-radius:6px; transition:width 0.6s cubic-bezier(0.16,1,0.3,1);"></div>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  }

  /**
   * Render Environmental Multiplier Factor comparison cards
   */
  function renderImpactFactors(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const factors = [
      { title: "College Fest / Event", impact: "+35% to +50%", desc: "High campus attendance creates massive spike in snack and biryani demand.", color: "#10b981", icon: "🎉" },
      { title: "Monsoon / Rainy Weather", impact: "+35% on Snacks", desc: "Heavy rain doubles hot snacks (Samosa & Chai) while reducing travel off campus.", color: "#3b82f6", icon: "🌧️" },
      { title: "Exam Period", impact: "+15% Quick Bites", desc: "Students favor quick sandwiches & tea over sit-down thali meals during study periods.", color: "#8b5cf6", icon: "📚" },
      { title: "College Holiday / Weekend", impact: "-35% to -50%", desc: "Hostel residents remain, but day-scholar demand drops substantially.", color: "#f59e0b", icon: "🏖️" }
    ];

    let html = `<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px;">`;
    factors.forEach(f => {
      html += `
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(75,85,99,0.3); border-radius:12px; padding:16px;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:20px;">${f.icon}</span>
            <span style="font-weight:600; font-size:13px; color:#f3f4f6;">${f.title}</span>
          </div>
          <div style="font-size:18px; font-weight:700; color:${f.color}; margin-bottom:6px;">${f.impact}</div>
          <div style="font-size:12px; color:#9ca3af; line-height:1.4;">${f.desc}</div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  }

  if (typeof window !== 'undefined') {
    window.FoodMLCharts = {
      renderTrendChart: renderTrendChart,
      renderBarChart: renderBarChart,
      renderImpactFactors: renderImpactFactors
    };
  }
  if (typeof globalThis !== 'undefined') {
    globalThis.FoodMLCharts = {
      renderTrendChart: renderTrendChart,
      renderBarChart: renderBarChart,
      renderImpactFactors: renderImpactFactors
    };
  }

  return {
    renderTrendChart: renderTrendChart,
    renderBarChart: renderBarChart,
    renderImpactFactors: renderImpactFactors
  };
})();