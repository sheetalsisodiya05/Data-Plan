import duckdb

# 1. Connect to DuckDB
con = duckdb.connect("sales.db")

print("DuckDB connected successfully!")

# 2. Create 2 million fake sales records
con.execute("""
    CREATE TABLE IF NOT EXISTS sales AS
    SELECT i AS id,
           ['US','UK','IN','DE'][1 + (i % 4)] AS country,
           (random() * 100)::DECIMAL(10,2) AS revenue
    FROM range(2_000_000) t(i)
""")

print("Sales table created!")

# 3. Check total records
count = con.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

print("Total records:", count)

# 4. OLAP query
print("\nOLAP QUERY - Revenue by country")

result = con.execute("""
    SELECT country, SUM(revenue)
    FROM sales
    GROUP BY country
""").fetchall()

print(result)

# 5. OLTP-shaped query
print("\nOLTP-SHAPED QUERY - Find one record")

result = con.execute("""
    SELECT *
    FROM sales
    WHERE id = 12345
""").fetchall()

print(result)

con.close()