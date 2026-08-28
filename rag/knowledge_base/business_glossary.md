# Business Logic & Metric Definitions

* **Churned Customer**: Any customer whose status is marked as `'churned'` or has not placed an order in the last 90 days.
* **Revenue / Sales**: Calculated strictly by summing `total_amount` in the `orders` table where `status = 'completed'`.
* **Average Order Value (AOV)**: `SUM(total_amount) / COUNT(order_id)` for completed orders.