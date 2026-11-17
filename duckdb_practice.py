import duckdb

con = duckdb.connect()

# Create 2 million fake sales records
con.execute("""
    CREATE TABLE sales AS
    SELECT i AS id,
           ['US','UK','IN','DE'][1 + (i % 4)] AS country,
           (random() * 100)::DECIMAL(10,2) AS revenue
    FROM range(2_000_000) t(i)
""")

# OLAP query
print("OLAP Query:")

print(
    con.execute("""
        SELECT country, SUM(revenue)
        FROM sales
        GROUP BY country
    """).fetchall()
)


# OLTP query
print("OLTP Query:")

print(
    con.execute("""
        SELECT *
        FROM sales
        WHERE id = 12345
    """).fetchall()
)

#---------------non-idempotent

con.execute("""
    CREATE TABLE report AS
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

before = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

# Append the same records again
con.execute("""
    INSERT INTO report
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

after = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("Before:", before)
print("After:", after)