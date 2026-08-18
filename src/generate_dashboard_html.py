import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "outputs/dashboard_data.json"
HTML_OUTPUT = ROOT / "outputs/interactive_dashboard.html"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

json_data_str = json.dumps(data["records"])

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Voltix Insights — 360° Omnichannel Retail Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg-dark: #070B14;
      --bg-card: #0F172A;
      --bg-card-hover: #17233D;
      --border-color: #1E293B;
      --accent-cyan: #38BDF8;
      --accent-emerald: #10B981;
      --accent-amber: #F59E0B;
      --accent-rose: #F43F5E;
      --accent-indigo: #818CF8;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --radius: 12px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      padding: 24px;
      min-height: 100vh;
    }
    .dashboard-container {
      max-width: 1600px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    /* Header */
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-color);
    }
    .header-title h1 {
      font-size: 26px;
      font-weight: 800;
      background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #10B981 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.5px;
    }
    .header-title p {
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 4px;
    }
    .header-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--accent-emerald);
      font-size: 13px;
      font-weight: 600;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      background-color: var(--accent-emerald);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-emerald);
    }

    /* Filters Bar */
    .filter-bar {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 16px 20px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
    }
    .filter-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .filter-label {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    select {
      background-color: #131E35;
      color: var(--text-main);
      border: 1px solid #28354E;
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 13.5px;
      font-weight: 500;
      cursor: pointer;
      outline: none;
      transition: all 0.2s ease;
    }
    select:hover, select:focus {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }
    .reset-btn {
      margin-left: auto;
      background: transparent;
      color: var(--accent-cyan);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .reset-btn:hover {
      background: rgba(56, 189, 248, 0.12);
      border-color: var(--accent-cyan);
    }

    /* KPI Ribbon */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
    }
    .kpi-card {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 20px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: #2E3E5B;
    }
    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
    }
    .card-sales::before { background: linear-gradient(90deg, #38BDF8, #818CF8); }
    .card-profit::before { background: linear-gradient(90deg, #10B981, #059669); }
    .card-margin::before { background: linear-gradient(90deg, #F59E0B, #D97706); }
    .card-aov::before { background: linear-gradient(90deg, #818CF8, #6366F1); }
    .card-orders::before { background: linear-gradient(90deg, #EC4899, #F43F5E); }
    
    .kpi-title {
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    .kpi-value {
      font-size: 28px;
      font-weight: 800;
      color: var(--text-main);
      margin: 8px 0 6px 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .kpi-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12.5px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .badge-positive {
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
    }
    .badge-healthy {
      background: rgba(56, 189, 248, 0.15);
      color: #38BDF8;
    }

    /* Main Chart Grid */
    .chart-grid-top {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
    }
    .chart-grid-bottom {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    @media (max-width: 1024px) {
      .chart-grid-top, .chart-grid-bottom {
        grid-template-columns: 1fr;
      }
    }
    .chart-card {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 22px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      display: flex;
      flex-direction: column;
    }
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }
    .chart-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
    }
    .chart-subtitle {
      font-size: 12.5px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .canvas-container {
      position: relative;
      flex: 1;
      min-height: 280px;
    }

    /* Data Table Section */
    .table-card {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 22px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 13.5px;
    }
    th {
      text-align: left;
      padding: 12px 14px;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-color);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: 0.5px;
    }
    td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(30, 41, 59, 0.6);
      color: var(--text-main);
    }
    tr:hover td {
      background-color: var(--bg-card-hover);
    }
    .margin-pill {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 12px;
    }
    .margin-pill.high { background: rgba(16, 185, 129, 0.18); color: #34D399; }
    .margin-pill.med { background: rgba(245, 158, 11, 0.18); color: #FBBF24; }
    .margin-pill.low { background: rgba(239, 68, 68, 0.18); color: #F87171; }
  </style>
</head>
<body>

<div class="dashboard-container">
  
  <!-- Header -->
  <header>
    <div class="header-title">
      <h1>⚡ Voltix Insights Dashboard</h1>
      <p>360° Omnichannel Retail Performance, Profitability & Margin Intelligence</p>
    </div>
    <div class="header-badge">
      <span class="pulse-dot"></span>
      <span>Live Interactive Data • 15,000 Records</span>
    </div>
  </header>

  <!-- Filter Bar -->
  <div class="filter-bar">
    <div class="filter-group">
      <span class="filter-label">Year:</span>
      <select id="filter-year" onchange="applyFilters()">
        <option value="ALL">All Years (2024 - 2025)</option>
        <option value="2024">2024</option>
        <option value="2025">2025</option>
      </select>
    </div>

    <div class="filter-group">
      <span class="filter-label">Channel:</span>
      <select id="filter-channel" onchange="applyFilters()">
        <option value="ALL">All Channels</option>
        <option value="Online">Online</option>
        <option value="Store">In-Store</option>
      </select>
    </div>

    <div class="filter-group">
      <span class="filter-label">Region:</span>
      <select id="filter-region" onchange="applyFilters()">
        <option value="ALL">All Regions</option>
        <option value="North">North</option>
        <option value="South">South</option>
        <option value="West">West</option>
        <option value="East">East</option>
      </select>
    </div>

    <div class="filter-group">
      <span class="filter-label">Category:</span>
      <select id="filter-category" onchange="applyFilters()">
        <option value="ALL">All Categories</option>
        <option value="Mobiles & Tablets">Mobiles & Tablets</option>
        <option value="Laptops & Computers">Laptops & Computers</option>
        <option value="Audio & Accessories">Audio & Accessories</option>
        <option value="Smart TVs & Appliances">Smart TVs & Appliances</option>
        <option value="Wearables & Fitness">Wearables & Fitness</option>
      </select>
    </div>

    <button class="reset-btn" onclick="resetFilters()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      Reset Filters
    </button>
  </div>

  <!-- KPI Ribbon -->
  <div class="kpi-grid">
    <div class="kpi-card card-sales">
      <div class="kpi-title">Total Revenue</div>
      <div class="kpi-value" id="kpi-sales">₹750.7M</div>
      <div class="kpi-badge badge-positive">▲ +14.2% YoY Growth</div>
    </div>

    <div class="kpi-card card-profit">
      <div class="kpi-title">Total Profit</div>
      <div class="kpi-value" id="kpi-profit">₹169.4M</div>
      <div class="kpi-badge badge-positive">▲ +11.8% YoY Growth</div>
    </div>

    <div class="kpi-card card-margin">
      <div class="kpi-title">Profit Margin %</div>
      <div class="kpi-value" id="kpi-margin">22.6%</div>
      <div class="kpi-badge badge-healthy" id="badge-margin-status">● Healthy Target</div>
    </div>

    <div class="kpi-card card-aov">
      <div class="kpi-title">Avg Order Value (AOV)</div>
      <div class="kpi-value" id="kpi-aov">₹50,045</div>
      <div class="kpi-badge badge-healthy">Per Order Average</div>
    </div>

    <div class="kpi-card card-orders">
      <div class="kpi-title">Total Volume</div>
      <div class="kpi-value" id="kpi-orders">15,000</div>
      <div class="kpi-badge badge-healthy" id="kpi-units">26,931 Units Sold</div>
    </div>
  </div>

  <!-- Charts Grid Top -->
  <div class="chart-grid-top">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Monthly Revenue & Profit Performance Trend</div>
          <div class="chart-subtitle">Revenue (Cyan Area) vs. Net Profit (Emerald Area)</div>
        </div>
      </div>
      <div class="canvas-container">
        <canvas id="trendChart"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Online vs. Store Channels</div>
          <div class="chart-subtitle">Revenue split by transaction medium</div>
        </div>
      </div>
      <div class="canvas-container">
        <canvas id="channelChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Charts Grid Bottom -->
  <div class="chart-grid-bottom">
    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Revenue & Margin by Category</div>
          <div class="chart-subtitle">Product category performance ranked by sales</div>
        </div>
      </div>
      <div class="canvas-container">
        <canvas id="categoryChart"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div>
          <div class="chart-title">Regional Performance Distribution</div>
          <div class="chart-subtitle">Total Revenue contribution by territory</div>
        </div>
      </div>
      <div class="canvas-container">
        <canvas id="regionChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Performance Table -->
  <div class="table-card">
    <div class="chart-header">
      <div>
        <div class="chart-title">Top Products & Profitability Health</div>
        <div class="chart-subtitle">Filtered breakdown of high-volume electronics and margin benchmarks</div>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Category</th>
          <th>Units Sold</th>
          <th>Total Sales (INR)</th>
          <th>Total Profit</th>
          <th>Profit Margin</th>
        </tr>
      </thead>
      <tbody id="product-table-body">
        <!-- Injected via JavaScript -->
      </tbody>
    </table>
  </div>

</div>

<script>
  // Complete Cleaned Dataset (15,000 Records)
  const RAW_DATA = __RAW_DATA_PLACEHOLDER__;

  let trendChart, channelChart, categoryChart, regionChart;

  function formatCurrency(val) {
    if (val >= 1e7) return "₹" + (val / 1e7).toFixed(1) + "Cr";
    if (val >= 1e6) return "₹" + (val / 1e6).toFixed(1) + "M";
    if (val >= 1e3) return "₹" + (val / 1e3).toFixed(0) + "K";
    return "₹" + Math.round(val).toLocaleString();
  }

  function initCharts() {
    Chart.defaults.color = "#94A3B8";
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    // 1. Monthly Trend Chart
    const ctxTrend = document.getElementById("trendChart").getContext("2d");
    trendChart = new Chart(ctxTrend, {
      type: "line",
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { position: "top", labels: { color: "#F8FAFC", font: { size: 12 } } }
        },
        scales: {
          x: { grid: { color: "rgba(51, 65, 85, 0.4)" } },
          y: {
            grid: { color: "rgba(51, 65, 85, 0.4)" },
            ticks: { callback: (v) => formatCurrency(v) }
          }
        }
      }
    });

    // 2. Channel Donut Chart
    const ctxChannel = document.getElementById("channelChart").getContext("2d");
    channelChart = new Chart(ctxChannel, {
      type: "doughnut",
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { color: "#F8FAFC", padding: 15 } }
        },
        cutout: "70%"
      }
    });

    // 3. Category Bar Chart
    const ctxCat = document.getElementById("categoryChart").getContext("2d");
    categoryChart = new Chart(ctxCat, {
      type: "bar",
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { color: "rgba(51, 65, 85, 0.4)" },
            ticks: { callback: (v) => formatCurrency(v) }
          },
          y: { grid: { display: false } }
        }
      }
    });

    // 4. Region Bar Chart
    const ctxRegion = document.getElementById("regionChart").getContext("2d");
    regionChart = new Chart(ctxRegion, {
      type: "bar",
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: "rgba(51, 65, 85, 0.4)" },
            ticks: { callback: (v) => formatCurrency(v) }
          }
        }
      }
    });

    applyFilters();
  }

  function applyFilters() {
    const year = document.getElementById("filter-year").value;
    const channel = document.getElementById("filter-channel").value;
    const region = document.getElementById("filter-region").value;
    const category = document.getElementById("filter-category").value;

    const filtered = RAW_DATA.filter(d => {
      if (year !== "ALL" && String(d.year) !== year) return false;
      if (channel !== "ALL" && d.channel !== channel) return false;
      if (region !== "ALL" && d.region !== region) return false;
      if (category !== "ALL" && d.category !== category) return false;
      return true;
    });

    updateKPIs(filtered);
    updateMonthlyTrend(filtered);
    updateChannelChart(filtered);
    updateCategoryChart(filtered);
    updateRegionChart(filtered);
    updateProductTable(filtered);
  }

  function updateKPIs(data) {
    const sales = data.reduce((acc, d) => acc + d.sales_amount, 0);
    const profit = data.reduce((acc, d) => acc + d.profit, 0);
    const units = data.reduce((acc, d) => acc + d.quantity, 0);
    const orders = new Set(data.map(d => d.order_id || d.month + d.sales_amount)).size;
    const margin = sales > 0 ? (profit / sales) * 100 : 0;
    const aov = orders > 0 ? sales / orders : 0;

    document.getElementById("kpi-sales").textContent = formatCurrency(sales);
    document.getElementById("kpi-profit").textContent = formatCurrency(profit);
    document.getElementById("kpi-margin").textContent = margin.toFixed(1) + "%";
    document.getElementById("kpi-aov").textContent = formatCurrency(aov);
    document.getElementById("kpi-orders").textContent = data.length.toLocaleString();
    document.getElementById("kpi-units").textContent = units.toLocaleString() + " Units Sold";

    const badge = document.getElementById("badge-margin-status");
    if (margin >= 25) {
      badge.textContent = "🟢 Premium Margin";
      badge.style.color = "#34D399";
    } else if (margin >= 18) {
      badge.textContent = "🟡 Healthy Margin";
      badge.style.color = "#FBBF24";
    } else {
      badge.textContent = "🔴 Low Margin Alert";
      badge.style.color = "#F87171";
    }
  }

  function updateMonthlyTrend(data) {
    const map = {};
    data.forEach(d => {
      const ym = d.year_month;
      if (!map[ym]) map[ym] = { sales: 0, profit: 0 };
      map[ym].sales += d.sales_amount;
      map[ym].profit += d.profit;
    });

    const labels = Object.keys(map).sort();
    const salesData = labels.map(k => map[k].sales);
    const profitData = labels.map(k => map[k].profit);

    trendChart.data.labels = labels;
    trendChart.data.datasets = [
      {
        label: "Total Sales",
        data: salesData,
        borderColor: "#38BDF8",
        backgroundColor: "rgba(56, 189, 248, 0.15)",
        fill: true,
        tension: 0.35,
        borderWidth: 2.5,
        pointRadius: 3
      },
      {
        label: "Total Profit",
        data: profitData,
        borderColor: "#10B981",
        backgroundColor: "rgba(16, 185, 129, 0.15)",
        fill: true,
        tension: 0.35,
        borderWidth: 2.5,
        pointRadius: 3
      }
    ];
    trendChart.update();
  }

  function updateChannelChart(data) {
    const map = {};
    data.forEach(d => {
      map[d.channel] = (map[d.channel] || 0) + d.sales_amount;
    });

    const labels = Object.keys(map);
    const values = labels.map(k => map[k]);

    channelChart.data.labels = labels;
    channelChart.data.datasets = [{
      data: values,
      backgroundColor: ["#38BDF8", "#10B981", "#818CF8"],
      borderColor: "#0F172A",
      borderWidth: 3
    }];
    channelChart.update();
  }

  function updateCategoryChart(data) {
    const map = {};
    data.forEach(d => {
      map[d.category] = (map[d.category] || 0) + d.sales_amount;
    });

    const sorted = Object.entries(map).sort((a, b) => b[1] - a[1]);
    const labels = sorted.map(s => s[0]);
    const values = sorted.map(s => s[1]);

    categoryChart.data.labels = labels;
    categoryChart.data.datasets = [{
      data: values,
      backgroundColor: "#38BDF8",
      borderRadius: 6
    }];
    categoryChart.update();
  }

  function updateRegionChart(data) {
    const map = {};
    data.forEach(d => {
      map[d.region] = (map[d.region] || 0) + d.sales_amount;
    });

    const labels = Object.keys(map);
    const values = labels.map(k => map[k]);

    regionChart.data.labels = labels;
    regionChart.data.datasets = [{
      data: values,
      backgroundColor: ["#818CF8", "#38BDF8", "#10B981", "#F59E0B"],
      borderRadius: 6
    }];
    regionChart.update();
  }

  function updateProductTable(data) {
    const map = {};
    data.forEach(d => {
      if (!map[d.product]) map[d.product] = { name: d.product, category: d.category, units: 0, sales: 0, profit: 0 };
      map[d.product].units += d.quantity;
      map[d.product].sales += d.sales_amount;
      map[d.product].profit += d.profit;
    });

    const sorted = Object.values(map).sort((a, b) => b.sales - a.sales).slice(0, 10);
    const tbody = document.getElementById("product-table-body");
    tbody.innerHTML = "";

    sorted.forEach(p => {
      const margin = p.sales > 0 ? (p.profit / p.sales) * 100 : 0;
      let pillClass = "med";
      if (margin >= 25) pillClass = "high";
      else if (margin < 18) pillClass = "low";

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="font-weight: 600; color: #F8FAFC;">${p.name}</td>
        <td style="color: #94A3B8;">${p.category}</td>
        <td>${p.units.toLocaleString()}</td>
        <td style="font-weight: 600; color: #38BDF8;">${formatCurrency(p.sales)}</td>
        <td style="font-weight: 600; color: #10B981;">${formatCurrency(p.profit)}</td>
        <td><span class="margin-pill ${pillClass}">${margin.toFixed(1)}%</span></td>
      `;
      tbody.appendChild(tr);
    });
  }

  function resetFilters() {
    document.getElementById("filter-year").value = "ALL";
    document.getElementById("filter-channel").value = "ALL";
    document.getElementById("filter-region").value = "ALL";
    document.getElementById("filter-category").value = "ALL";
    applyFilters();
  }

  window.addEventListener("DOMContentLoaded", initCharts);
</script>

</body>
</html>
"""

html_content = html_template.replace("__RAW_DATA_PLACEHOLDER__", json_data_str)

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone Voltix Insights interactive dashboard at {HTML_OUTPUT}")
