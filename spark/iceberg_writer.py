"""Читает JSON из MinIO, пишет в Iceberg таблицу bronze.events_raw."""
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, to_date, col

spark = (
    SparkSession.builder
    .appName("BronzeIngest")
    .config("spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.3,"
            "org.apache.hadoop:hadoop-aws:3.3.4")
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.iceberg.type", "hadoop")
    .config("spark.sql.catalog.iceberg.warehouse", "s3a://lakehouse/warehouse")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .getOrCreate()
)

spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.bronze")

df = (
    spark.read.json("s3a://raw-bucket/events/date=*/*.json")
    .withColumn("ingested_at", current_timestamp())
    .withColumn("source_file", input_file_name())
    .withColumn("event_date", to_date(col("timestamp")))
)

(
    df.writeTo("iceberg.bronze.events_raw")
      .partitionedBy("event_date")
      .createOrReplace()
)

print("✅ Bronze written")
spark.stop()
