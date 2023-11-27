from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, json_tuple

# Initialize Spark session
spark = SparkSession.builder.appName("Kafka2MongoDB").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Define the Kafka source configuration
kafka_bootstrap_servers = "kafka:9092"
kafka_topic = "postgres.public.sample_table"

# Read from Kafka
raw_stream = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("subscribe", kafka_topic)
    .option("startingOffsets", "earliest")
    .option("includeTimestamp", True)
    .load()
)

# Aggregate the results
windowed_counts = (
    raw_stream
    .withColumn('result', json_tuple(col('value').cast('string'), "payload"))
    .withColumn('value_before', json_tuple(col('result'), "before"))
    .filter(col('value_before').isNull())
    .groupBy(window("timestamp", "10 seconds"))
    .count()
    .withColumnRenamed('count', 'number_of_new_records')
)

# Write the aggregated results to MongoDB
mongo_uri = "mongodb://mongo_admin:mongo_admin_password@host.docker.internal:27017"
mongo_database = "mongo_database"
mongo_collection = "aggregated_results"

query = (
    windowed_counts
    .writeStream
    .format("mongodb")
    .option("checkpointLocation", "/tmp/pyspark/")
    .option("forceDeleteTempCheckpointLocation", "true")
    .option("connection.uri", mongo_uri)
    .option("database", mongo_database)
    .option("collection", mongo_collection)
    .outputMode("complete")
    .start()
)

query.awaitTermination()
