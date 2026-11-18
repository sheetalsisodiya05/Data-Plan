import duckdb

# 1. Connect to DuckDB
con = duckdb.connect("employees.db")

print("DuckDB connected successfully!")


# 2. Delete old table if it exists
con.execute("DROP TABLE IF EXISTS employees")


# 3. Create employee table
con.execute("""
    CREATE TABLE employees (
        id INTEGER,
        name VARCHAR,
        department VARCHAR,
        salary INTEGER
    )
""")

print("Employee table created!")


# 4. Insert 25 employees manually
con.execute("""
    INSERT INTO employees VALUES
    (1, 'Akshay', 'IT', 75000),
    (2, 'Rahul', 'HR', 45000),
    (3, 'Priya', 'Finance', 85000),
    (4, 'Amit', 'IT', 95000),
    (5, 'Neha', 'Marketing', 55000),
    (6, 'Rohit', 'Sales', 60000),
    (7, 'Sneha', 'IT', 90000),
    (8, 'Vikas', 'HR', 50000),
    (9, 'Pooja', 'Finance', 80000),
    (10, 'Karan', 'Sales', 65000),
    (11, 'Anjali', 'Marketing', 70000),
    (12, 'Suresh', 'IT', 110000),
    (13, 'Manish', 'Finance', 75000),
    (14, 'Riya', 'HR', 48000),
    (15, 'Deepak', 'Sales', 72000),
""")

print("15 Employees inserted successfully!")


# 5. Check total employees
print("\nTOTAL EMPLOYEES")

result = con.execute("""
    SELECT COUNT(*) FROM employees
""").fetchone()

print(result)


# OPERATION 1: Find employee with maximum salary
print("\n1. HIGHEST SALARY")

result = con.execute("""
    SELECT *
    FROM employees
    ORDER BY salary DESC
    LIMIT 1
""").fetchall()

print(result)


# OPERATION 2: Find top 5 highest-paid employees
print("\n2. TOP 5 HIGHEST-PAID EMPLOYEES")

result = con.execute("""
    SELECT *
    FROM employees
    ORDER BY salary DESC
    LIMIT 5
""").fetchall()

print(result)


# OPERATION 3: Average salary by department
print("\n3. AVERAGE SALARY BY DEPARTMENT")

result = con.execute("""
    SELECT department, AVG(salary)
    FROM employees
    GROUP BY department
""").fetchall()

print(result)


# OPERATION 4: Total salary expenditure by department
print("\n4. TOTAL SALARY BY DEPARTMENT")

result = con.execute("""
    SELECT department, SUM(salary)
    FROM employees
    GROUP BY department
""").fetchall()

print(result)


# OPERATION 5: Find employee using ID
print("\n5. FIND EMPLOYEE BY ID")

result = con.execute("""
    SELECT *
    FROM employees
    WHERE id = 12
""").fetchall()

print(result)




# 6. Close connection
con.close()

print("\nDuckDB connection closed!")