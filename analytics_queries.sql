-- Query 1: Monthly Sales Drill-Down
-- Drill from Year -> Quarter -> Month
SELECT 
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.total_amount) as total_sales,
    SUM(f.quantity_sold) as units_moved
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.month_name
ORDER BY d.year, d.quarter;

-- Query 2: Top 10 Products by Revenue (with Percentage)
SELECT 
    p.product_name,
    p.category,
    SUM(f.total_amount) as revenue,
    CONCAT(ROUND(SUM(f.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM fact_sales), 2), '%') as rev_share
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- Query 3: Customer Segmentation
-- Group customers by High/Medium/Low value
SELECT 
    CASE 
        WHEN SUM(f.total_amount) > 50000 THEN 'High Value'
        WHEN SUM(f.total_amount) BETWEEN 20000 AND 50000 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,
    COUNT(DISTINCT f.customer_key) as customer_count,
    AVG(f.total_amount) as avg_transaction_value
FROM fact_sales f
GROUP BY customer_segment;