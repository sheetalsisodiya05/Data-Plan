import duckdb

con = duckdb.connect("sales.db")

# 1. Create report table
con.execute("""
    CREATE TABLE IF NOT EXISTS report AS
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

# 2. Check initial count
before = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("Before insertion:", before)

# 3. Insert duplicate records
con.execute("""
    INSERT INTO report
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

# 4. Check duplicate count
after = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("After insertion:", after)

# 5. Fix: Delete existing US records
con.execute("""
    DELETE FROM report
    WHERE country = 'US'
""")

# 6. Insert fresh records
con.execute("""
    INSERT INTO report
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

count1 = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("After first fix:", count1)

# 7. Repeat the same operation
con.execute("""
    DELETE FROM report
    WHERE country = 'US'
""")

con.execute("""
    INSERT INTO report
    SELECT *
    FROM sales
    WHERE country = 'US'
""")

count2 = con.execute(
    "SELECT COUNT(*) FROM report"
).fetchone()[0]

print("After second fix:", count2)

con.close()