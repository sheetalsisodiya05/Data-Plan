
import duckdb

con = duckdb.connect()


con.execute("""
    CREATE TABLE sales AS
    SELECT
        i AS id,
        ['US','UK','IN','DE'][1 + (i % 4)] AS country,
        (random() * 100)::DECIMAL(10,2) AS revenue
    FROM range(2000000) t(i)
""")

olap_result = con.execute("""
    SELECT country, SUM(revenue)
    FROM sales
    GROUP BY country
""").fetchall()

print("OLAP Result:", olap_result)

# OLTP-shaped: Retrieve one specific transaction
oltp_result = con.execute("""
    SELECT * FROM sales WHERE id = 12345
""").fetchall()

print("Single Transaction:", oltp_result)

con.execute("""
    CREATE TABLE report AS
    SELECT * FROM sales WHERE country = 'US'
""")

before = con.execute("SELECT COUNT(*) FROM report").fetchone()[0]

# Non-idempotent: Appending the same data again
con.execute("""
    INSERT INTO report
    SELECT * FROM sales WHERE country = 'US'
""")

after = con.execute("SELECT COUNT(*) FROM report").fetchone()[0]

print("\nNon-idempotent execution:")
print("Before:", before)
print("After:", after)


con.execute("""
    CREATE OR REPLACE TABLE report AS
    SELECT * FROM sales WHERE country = 'US'
""")

fixed_count_1 = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

# Run exactly the same operation again
con.execute("""
    CREATE OR REPLACE TABLE report AS
    SELECT * FROM sales WHERE country = 'US'
""")

fixed_count_2 = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("\nIdempotent execution:")
print("First execution:", fixed_count_1)
print("Second execution:", fixed_count_2)

assert fixed_count_1 == fixed_count_2

print("\nAll exercises completed successfully!")
