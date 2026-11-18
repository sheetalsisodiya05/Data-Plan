from database import con

with open("sql-modeling/queries/basic_sql.sql") as file:
    query = file.read()

result = con.execute(query).fetchall()

print(result)