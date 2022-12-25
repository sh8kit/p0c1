from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .appName("delta_spark").enableHiveSupport().getOrCreate()
df= spark.read.parquet("/Users/dani/Downloads/user_events+0+0000002200.snappy.parquet")
df.show()