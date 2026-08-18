USE sales_insights;

-- Overall KPIs
SELECT ROUND(SUM(sales_amount),2) total_sales,
       ROUND(SUM(profit),2) total_profit,
       COUNT(DISTINCT order_id) total_orders,
       SUM(quantity) units_sold,
       ROUND(SUM(profit)/SUM(sales_amount)*100,2) profit_margin_pct,
       ROUND(SUM(sales_amount)/COUNT(DISTINCT order_id),2) avg_order_value
FROM sales_transactions;

-- Monthly trend
SELECT year_month, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit,
       COUNT(DISTINCT order_id) orders
FROM sales_transactions
GROUP BY year_month ORDER BY year_month;

-- Category performance
SELECT category, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)/SUM(sales_amount)*100,2) margin_pct
FROM sales_transactions
GROUP BY category ORDER BY sales DESC;

-- Top products
SELECT product, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit, SUM(quantity) units
FROM sales_transactions
GROUP BY product ORDER BY sales DESC LIMIT 10;

-- Regional performance
SELECT region, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit,
       COUNT(DISTINCT order_id) orders
FROM sales_transactions
GROUP BY region ORDER BY sales DESC;

-- Channel performance
SELECT channel, COUNT(DISTINCT order_id) orders,
       ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)/SUM(sales_amount)*100,2) margin_pct
FROM sales_transactions GROUP BY channel ORDER BY sales DESC;

-- Top customers
SELECT customer_id, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit, COUNT(DISTINCT order_id) orders
FROM sales_transactions
GROUP BY customer_id ORDER BY sales DESC LIMIT 20;

-- MoM growth using LAG
WITH monthly AS (
    SELECT year_month, SUM(sales_amount) sales
    FROM sales_transactions GROUP BY year_month
)
SELECT year_month, ROUND(sales,2) sales,
       ROUND((sales-LAG(sales) OVER(ORDER BY year_month)) /
       NULLIF(LAG(sales) OVER(ORDER BY year_month),0)*100,2) mom_growth_pct
FROM monthly ORDER BY year_month;

-- Rank products within each category
WITH ps AS (
    SELECT category, product, SUM(sales_amount) sales
    FROM sales_transactions GROUP BY category, product
)
SELECT category, product, ROUND(sales,2) sales,
       DENSE_RANK() OVER(PARTITION BY category ORDER BY sales DESC) category_rank
FROM ps ORDER BY category, category_rank;

-- High-sales / low-margin products
SELECT product, ROUND(SUM(sales_amount),2) sales,
       ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)/SUM(sales_amount)*100,2) margin_pct
FROM sales_transactions
GROUP BY product
HAVING SUM(sales_amount) > (
    SELECT AVG(product_sales) FROM (
        SELECT SUM(sales_amount) product_sales
        FROM sales_transactions GROUP BY product
    ) x
)
AND SUM(profit)/SUM(sales_amount) < 0.18
ORDER BY sales DESC;
