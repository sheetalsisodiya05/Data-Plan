from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("EmployeeAnalysis") \
    .master("local[*]") \
    .config("spark.ui.enabled", "true") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

# Read CSV file
df = spark.read.csv(
    "data/employees.csv",
    header=True,
    inferSchema=True
)

df.cache()

df.count()
df.groupBy("department").count().show()

input("press enter")
spark.stop()