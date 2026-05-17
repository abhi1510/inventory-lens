-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) UNIQUE NOT NULL,
    product_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create inventory table
CREATE TABLE IF NOT EXISTS inventory (
    product_id VARCHAR(100) PRIMARY KEY,
    stock INTEGER NOT NULL,
    min_stock INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    ordered_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE inventory
ADD CONSTRAINT fk_inventory_product
FOREIGN KEY (product_id)
REFERENCES products(product_id)
ON DELETE CASCADE;

ALTER TABLE orders
ADD CONSTRAINT fk_orders_product
FOREIGN KEY (product_id)
REFERENCES products(product_id)
ON DELETE CASCADE;