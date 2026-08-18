CREATE DATABASE IF NOT EXISTS sales_insights;
USE sales_insights;

DROP TABLE IF EXISTS sales_transactions;

CREATE TABLE sales_transactions (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    state VARCHAR(50), city VARCHAR(50), region VARCHAR(20),
    channel VARCHAR(20), category VARCHAR(50), product VARCHAR(100),
    quantity INT, unit_price DECIMAL(12,2), discount_pct DECIMAL(6,4),
    unit_cost DECIMAL(12,2), sales_amount DECIMAL(14,2),
    cost_amount DECIMAL(14,2), profit DECIMAL(14,2),
    payment_mode VARCHAR(30), year INT, month_num INT, month VARCHAR(10),
    quarter VARCHAR(5), year_month VARCHAR(7),
    gross_sales_before_discount DECIMAL(14,2),
    discount_amount DECIMAL(14,2), profit_margin DECIMAL(10,6)
);

-- Import data after creating the table:
-- LOAD DATA LOCAL INFILE 'data/processed/sales_transactions_clean.csv'
-- INTO TABLE sales_transactions
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- IGNORE 1 ROWS;
