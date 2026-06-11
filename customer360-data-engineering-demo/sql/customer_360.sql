DROP TABLE IF EXISTS customer_360;

CREATE TABLE customer_360 AS
WITH order_features AS (
    SELECT
        customer_id,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
        SUM(CASE WHEN status = 'completed' THEN order_amount ELSE 0 END) AS total_revenue,
        MAX(order_date) AS last_order_date,
        COUNT(CASE WHEN status = 'returned' THEN 1 END) AS returned_orders
    FROM orders
    GROUP BY customer_id
),
web_features AS (
    SELECT
        customer_id,
        COUNT(*) AS web_events,
        COUNT(DISTINCT session_id) AS web_sessions,
        COUNT(CASE WHEN event_type = 'checkout' THEN 1 END) AS checkout_events
    FROM web_events
    GROUP BY customer_id
),
support_features AS (
    SELECT
        customer_id,
        COUNT(*) AS support_tickets,
        AVG(resolved_hours) AS avg_resolution_hours,
        MAX(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) AS had_high_priority_ticket
    FROM support_tickets
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.signup_date,
    c.signup_channel,
    c.loyalty_tier,
    c.country,
    COALESCE(o.completed_orders, 0) AS completed_orders,
    ROUND(COALESCE(o.total_revenue, 0), 2) AS total_revenue,
    COALESCE(o.returned_orders, 0) AS returned_orders,
    COALESCE(w.web_events, 0) AS web_events,
    COALESCE(w.web_sessions, 0) AS web_sessions,
    COALESCE(w.checkout_events, 0) AS checkout_events,
    COALESCE(s.support_tickets, 0) AS support_tickets,
    ROUND(COALESCE(s.avg_resolution_hours, 0), 2) AS avg_resolution_hours,
    COALESCE(s.had_high_priority_ticket, 0) AS had_high_priority_ticket,
    CASE
        WHEN COALESCE(o.completed_orders, 0) <= 1
          AND COALESCE(w.checkout_events, 0) = 0
          AND COALESCE(s.had_high_priority_ticket, 0) = 1
        THEN 1
        ELSE 0
    END AS churn_label
FROM customers c
LEFT JOIN order_features o ON c.customer_id = o.customer_id
LEFT JOIN web_features w ON c.customer_id = w.customer_id
LEFT JOIN support_features s ON c.customer_id = s.customer_id;
