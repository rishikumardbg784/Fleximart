-- Query 1: Customer Purchase History
-- Question: Customers with 2+ orders and >5000 spent
SELECT 
    c.first_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) >= 2 AND SUM(o.total_amount) > 5000
ORDER BY total_spent DESC;

-- Query 2: Product Sales Analysis
-- Question: Categories with >10000 revenue
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) as num_products,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.subtotal) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
HAVING total_revenue > 10000
ORDER BY total_revenue DESC;

-- Query 3: Monthly Sales Trend
-- Question: Monthly breakdown with Cumulative Revenue (Running Total)
SELECT 
    DATE_FORMAT(order_date, '%M') as month_name,
    COUNT(order_id) as total_orders,
    SUM(total_amount) as monthly_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY MONTH(order_date)) as cumulative_revenue
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY MONTH(order_date), month_name
ORDER BY MONTH(order_date);