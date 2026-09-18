# Voltix Insights — Power BI Dashboard Build Guide
**Project:** 360° Omnichannel Retail & Profitability Intelligence Pipeline  
**Theme:** Executive Dark Slate & Electric Cyan/Emerald  

---

## Phase 1: Environment & Theme Setup

### 1. Data Ingestion
1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV** $\rightarrow$ Select [`data/processed/sales_transactions_clean.csv`](file:///c:/Users/HP/Downloads/Sales_Insights_End_to_End/sales_insights_end_to_end/data/processed/sales_transactions_clean.csv).
3. In Power Query Editor:
   - Ensure `order_date` is formatted as **Date**.
   - Ensure `sales_amount`, `profit`, `unit_price`, and `cost_amount` are **Fixed Decimal Number (Currency)**.
   - Rename the query/table to **`Sales`**.
   - Click **Close & Apply**.

### 2. Import Custom Theme (1-Click Styling)
1. Go to the top ribbon $\rightarrow$ **View** tab.
2. In the Themes dropdown, click **Browse for themes...**.
3. Select [`powerbi/sales_insights_theme.json`](file:///c:/Users/HP/Downloads/Sales_Insights_End_to_End/sales_insights_end_to_end/powerbi/sales_insights_theme.json).
4. *Result:* Your canvas background automatically turns dark slate (`#0B0F19`), cards receive rounded corners with subtle drop shadows, and visuals adopt curated accent colors (`#38BDF8`, `#10B981`, `#818CF8`).

### 3. Star Schema Data Modeling
1. Go to **Modeling** tab $\rightarrow$ Click **New Table**.
2. Copy and paste the **`Date`** table DAX formula from [`powerbi/DAX_measures.txt`](file:///c:/Users/HP/Downloads/Sales_Insights_End_to_End/sales_insights_end_to_end/powerbi/DAX_measures.txt).
3. Right-click the `Date` table $\rightarrow$ **Mark as Date Table** $\rightarrow$ Select `Date[Date]`.
4. In `Date` table, select `Month Short` $\rightarrow$ Under **Column tools**, set **Sort by Column** $\rightarrow$ `Month Number`.
5. In Model View, create an active 1-to-many relationship:
   $$\mathbf{Date[Date]\;(1)} \longrightarrow \mathbf{Sales[order\_date]\;(*)}$$

---

## Phase 2: Page-by-Page Visual Wireframes

```
+-----------------------------------------------------------------------------------------------+
|  HEADER: Executive Sales Insights Dashboard            | [Year Slicer] [Channel Slicer]   |
+-----------------------------------------------------------------------------------------------+
| [ Total Sales ]       | [ Total Profit ]      | [ Profit Margin % ]   | [ Average Order Val ] |
| ₹750.7M (▲ +14.2%)    | ₹169.4M (▲ +11.8%)    | 22.6% (🟢 Healthy)    | ₹50,045 (▲ +2.1%)     |
+-----------------------+-----------------------+-----------------------+-----------------------+
|  MONTHLY SALES & PROFIT TREND (Line & Area)   |  CATEGORY PERFORMANCE (Horizontal Bar Chart)  |
|                                               |                                               |
|  - Sales (Cyan Line with data dots)           |  - Mobiles & Tablets (₹310M)                  |
|  - Profit (Emerald Gradient Area)             |  - Laptops & Computers (₹245M)                |
|                                               |  - Audio & Accessories (₹112M)                |
+-----------------------------------------------+-----------------------------------------------+
|  REGIONAL SALES (Donut / Bar)                 |  ONLINE VS STORE CHANNELS (100% Stacked Bar)  |
|  - North / South / West / East                |  - Revenue split & Margin comparison          |
+-----------------------------------------------------------------------------------------------+
```

---

### Page 1: Executive Overview (`16:9 Canvas`)

1. **Top Navigation & KPI Ribbon (Top 18% of Canvas)**:
   - Use the **New Card Visual** to show 4 primary KPIs:
     - **Card 1 (Total Sales):** Value: `[Total Sales]`, Subtitle: `[Sales KPI Subtitle]` (shows `▲ +% vs LY`).
     - **Card 2 (Total Profit):** Value: `[Total Profit]`, Subtitle: `[Profit KPI Subtitle]`.
     - **Card 3 (Profit Margin):** Value: `[Profit Margin %]`, Subtitle: `[Margin Health Badge]`.
     - **Card 4 (AOV):** Value: `[Average Order Value]`.
   - Add a slicer bar on top-right: `Date[Year]` (Dropdown or Tile) and `Sales[channel]` (Pill buttons).

2. **Monthly Sales Trend (Line and Stacked Column Chart or Area Chart)**:
   - **X-Axis:** `Date[Year Month]`
   - **Line Y-Axis:** `[Total Sales]` (Cyan `#38BDF8`)
   - **Column Y-Axis:** `[Total Profit]` (Emerald `#10B981`)
   - *Design Tip:* Turn on data markers on the line and enable smooth line curves.

3. **Category Breakdown (Clustered Bar Chart)**:
   - **Y-Axis:** `Sales[category]`
   - **X-Axis:** `[Total Sales]`
   - **Tooltips:** `[Total Profit]`, `[Profit Margin %]`, `[Units Sold]`.
   - *Design Tip:* Add data labels inside base with currency formatting `₹#,##0.0M`.

4. **Channel & Region Split (Donut Chart & Matrix)**:
   - **Donut Visual:** Legend: `Sales[channel]`, Values: `[Total Sales]`.
   - Shows Online (60%+) vs In-Store (35%+) distribution.

---

### Page 2: Product & Margin Deep Dive

1. **Sales vs. Profit Margin Matrix (Scatter Plot)**:
   - **X-Axis:** `[Total Sales]`
   - **Y-Axis:** `[Profit Margin %]` (Format as `%`)
   - **Size:** `[Units Sold]`
   - **Values (Legend):** `Sales[product]`
   - *Actionable Insight:* Clearly flags high-sales / low-margin products in the bottom-right quadrant!

2. **Top 10 Products by Revenue (Horizontal Bar Chart)**:
   - Filter: Top 10 by `[Total Sales]`.
   - Bar color: Use Conditional Formatting $\rightarrow$ Field Value $\rightarrow$ `[Color_Margin_Status]` (Emerald for healthy, Red for alert).

3. **Low-Margin Alert Table (Grid Table)**:
   - Columns: `product`, `category`, `Total Sales`, `Total Profit`, `Profit Margin %`, `Average Discount %`.
   - Filter visual: `[Profit Margin %] < 0.18`.
   - Conditional formatting: Background color scale on `Average Discount %` to show correlation between heavy discounting and profit loss.

---

### Page 3: Customer & Channel Dynamics

1. **Customer Concentration Pareto (Table)**:
   - Columns: `customer_id`, `Total Orders`, `Total Sales`, `Total Profit`, `Average Order Value`.
   - Sort by `Total Sales` descending.
2. **Channel Performance Comparison (Clustered Column Chart)**:
   - **X-Axis:** `Sales[channel]`
   - **Y-Axis:** `[Total Sales]`, `[Total Profit]`
3. **Payment Mode Breakdown (Treemap / Donut)**:
   - Group: `Sales[payment_mode]`
   - Values: `[Total Sales]`

---

### Page 4: Regional Analysis & Drill-Through

1. **State-Level Performance (Shape Map / Filled Map or Matrix)**:
   - Location: `Sales[state]`
   - Color Saturation / Value: `[Total Sales]`
2. **City Drill-Through Page**:
   - Create a dedicated hidden page named **`City Drillthrough`**.
   - Add `Sales[state]` to the **Drill-through** field bucket.
   - Add a back button, city performance table, and top customer list for that selected state.

---

## Phase 3: Modern Polish & Pro-Features

### 1. Interactive Tooltip Page (Hover Details)
1. Add a new page named **`Tooltip_ProductPreview`**.
2. In Page formatting $\rightarrow$ **Page Information** $\rightarrow$ Set **Allow use as tooltip = On**.
3. Set Canvas size to **Tooltip (320 x 240 px)**.
4. Add a mini top-3 product bar chart.
5. On Page 1 Category chart $\rightarrow$ Visual Formatting $\rightarrow$ Tooltips $\rightarrow$ Page: Select `Tooltip_ProductPreview`.
6. *Result:* When hovering over any category in the overview page, an instant mini-breakdown appears!

### 2. Reset All Slicers Button
1. Clear all slicers on the page.
2. Go to **View** $\rightarrow$ **Bookmarks** $\rightarrow$ Click **Add Bookmark** $\rightarrow$ Name it `ResetFilters`.
3. Insert **Button** $\rightarrow$ Blank / Icon $\rightarrow$ Set Text: `"↺ Reset Filters"`.
4. Action: **Bookmark** $\rightarrow$ Select `ResetFilters`.
