
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

# Create Spark application
spark = (
    SparkSession.builder
    .appName("PySpark-Learning")
    .master("local[*]")
    .config("spark.ui.enabled", "true")
    .config("spark.ui.port", "4040")
    .getOrCreate()
)

# Sample data
data = [
    (1, "Satya", "IT", 45000),
    (2, "Rahul", "HR", 35000),
    (3, "Amit", "IT", 55000),
    (4, "Priya", "Finance", 50000),
    (5, "Neha", "HR", 40000)
]

columns = ["id", "name", "department", "salary"]

df = spark.createDataFrame(data, columns)

print("Spark Version:", spark.version)

df.show()

# Transformation
result = (
    df.groupBy("department")
    .agg(
        count("*").alias("employees"),
        avg("salary").alias("average_salary")
    )
)

# Action: triggers execution
result.show()

# Keep application alive until finished
input("Press Enter to stop Spark...")

spark.stop()
