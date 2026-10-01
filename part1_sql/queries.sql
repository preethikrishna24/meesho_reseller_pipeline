-- Part 1: Meesho reseller-operations standing queries.
-- Run against data/meesho_reseller.db.

-- 1. Monthly revenue by category
SELECT month,
       category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
         CASE category
           WHEN 'Ethnic Wear' THEN 1
           WHEN 'Western Wear' THEN 2
           WHEN 'Kids Wear' THEN 3
           WHEN 'Home & Kitchen' THEN 4
           WHEN 'Beauty & Personal Care' THEN 5
         END;

-- 2. Region-wise total revenue and order count
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;

-- 3. Top resellers by total spend (> 50000), descending, top 5
SELECT r.reseller_id,
       r.reseller_name,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders AS o
JOIN resellers AS r ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- 4a. Resellers who have never placed an order.
SELECT r.reseller_id,
       r.reseller_name,
       r.region
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE o.order_id IS NULL
ORDER BY r.reseller_id;

-- 4b. Demonstration of COUNT(*) vs COUNT(order_id) for the zero-order reseller.
-- COUNT(*) counts the single NULL-extended LEFT JOIN row as 1.
-- COUNT(order_id) counts only non-NULL order IDs, so the true match count is 0.
SELECT r.reseller_id,
       COUNT(*) AS row_count,
       COUNT(o.order_id) AS order_id_count
FROM resellers AS r
LEFT JOIN orders AS o ON o.reseller_id = r.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- 5. June Delivered AOV
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
