
import duckdb

# Connect to DuckDB
con = duckdb.connect()

# Create a sales table with 2 million records
con.execute("""
    CREATE TABLE sales AS
    SELECT
        i AS id,
        ['US', 'UK', 'IN', 'DE'][1 + (i % 4)] AS country,
        (random() * 100)::DECIMAL(10,2) AS revenue
    FROM range(2000000) t(i)
""")

print("Sales table created successfully!")

# OLAP QUERY: Analyze total revenue country-wise
print("\n--- OLAP: Total Revenue by Country ---")

olap_result = con.execute("""
    SELECT country, SUM(revenue)
    FROM sales
    GROUP BY country
""").fetchall()

print(olap_result)


# OLTP-SHAPED QUERY: Find one particular record
print("\n--- OLTP-shaped: Find One Sale ---")

oltp_result = con.execute("""
    SELECT *
    FROM sales
    WHERE id = 12345
""").fetchall()

print(oltp_result)
