
import duckdb

con = duckdb.connect("sql_practice.db")

con.execute("""
CREATE OR REPLACE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    country VARCHAR,
    signup_date DATE
);

CREATE OR REPLACE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR
);

CREATE OR REPLACE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_date DATE,
    amount DECIMAL(10,2),
    method VARCHAR
);

INSERT INTO customers VALUES
(1, 'Mara', 'US', '2025-01-01'),
(2, 'Ito', 'JP', '2025-01-05'),
(3, 'Lena', 'US', '2025-02-01'),
(4, 'John', 'IN', '2025-02-10'),
(5, 'Sara', 'IN', '2025-03-01');

INSERT INTO orders VALUES
(101, 1, '2025-03-01', 500, 'Completed'),
(102, 1, '2025-03-05', 300, 'Completed'),
(103, 1, '2025-03-10', 200, 'Pending'),
(104, 2, '2025-03-02', 900, 'Completed'),
(105, 2, '2025-03-08', 400, 'Cancelled'),
(106, 3, '2025-03-03', 700, 'Completed'),
(107, 4, '2025-03-09', 600, 'Pending');

INSERT INTO payments VALUES
(1, 101, '2025-03-01', 500, 'Card'),
(2, 102, '2025-03-05', 300, 'UPI'),
(3, 104, '2025-03-02', 900, 'Card'),
(4, 106, '2025-03-03', 700, 'UPI'),
(5, 106, '2025-03-04', 200, 'Card');
""")

print("Database ready!")
