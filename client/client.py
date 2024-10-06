import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType


def client():
    print('Starting PySpark client to process MQTT data stream')

    # Initialize Spark session
    spark = SparkSession.builder.appName("WeatherDataSQL").getOrCreate()
    schema = StructType([
        StructField("stationId", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("windSpeed", DoubleType(), True),
        StructField("pressure", DoubleType(), True)
    ])

    # Connect to the socket server
    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # # Process the data (here, we split each line by space and count words)
    # words = lines.select(explode(split(lines.value, " ")).alias("word"))
    # wordCounts = words.groupBy("word").count()

    # # Output the results to the console
    # query = wordCounts \
    #     .writeStream \
    #     .outputMode("complete") \
    #     .format("console") \
    #     .start()

    # Create an RDD from the sample data
    rdd = spark.sparkContext.parallelize(lines)
    json_df = spark.read.json(rdd, schema=schema)

    # Convert JSON strings to structured DataFrame based on the schema
    weather_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

    # Register DataFrame as a SQL temporary view
    weather_df.createOrReplaceTempView("weather_data")

    # Example SQL query on the data
    query = spark.sql("SELECT stationId, temperature, humidity, windSpeed, pressure FROM weather_data WHERE temperature > 30")
    query.show()

    query.awaitTermination()


sys.modules[__name__] = client

