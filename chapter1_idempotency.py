
import duckdb

con = duckdb.connect()

# Create sample sales data
con.execute("""
    CREATE TABLE sales AS
    SELECT *
    FROM (
        VALUES
        (1, 'US', 100),
        (2, 'US', 200),
        (3, 'UK', 300),
        (4, 'US', 400),
        (5, 'IN', 500)
    ) AS t(id, country, revenue)
""")

# Create an empty report table
con.execute("""
    CREATE TABLE report AS
    SELECT * FROM sales WHERE country = 'US'
    LIMIT 0
""")

# First run
con.execute("""
    INSERT INTO report
    SELECT * FROM sales
    WHERE country = 'US'
""")

before = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

# Second run: accidentally inserts the same data again
con.execute("""
    INSERT INTO report
    SELECT * FROM sales
    WHERE country = 'US'
""")

after = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("Records after first run:", before)
print("Records after second run:", after)
