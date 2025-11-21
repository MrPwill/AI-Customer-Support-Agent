-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL, -- e.g., 'ORD-123'
    user_id INTEGER REFERENCES users(id),
    product_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'shipped', 'processing', 'delivered', 'cancelled'
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP
);

-- Support Tickets table
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL, -- e.g., 'TKT-001'
    user_id INTEGER REFERENCES users(id),
    subject VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'in_progress', 'resolved', 'closed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
