from functools import lru_cache
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


@lru_cache()
def get_delta_spark():
    builder = SparkSession \
        .builder \
        .appName("delta_spark") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.1") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    return configure_spark_with_delta_pip(builder).enableHiveSupport().getOrCreate()


def create_new_storage_table(table):
    spark = get_delta_spark()
    create_table_ddl = table.generate_ddl()

    spark.sql(create_table_ddl)

def run_query(query):
    spark = get_delta_spark()
    spark.sql(query)