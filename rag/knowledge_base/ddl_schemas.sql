CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' --Values: 'active', 'churned', 'suspended'
);

CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERNECES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed' --Values: 'pending', 'completed', 'cancelled'
);

CREATE TABLE order_items(
    item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES order(order_id),
    product_name VARCHAR(100) N0T NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
)