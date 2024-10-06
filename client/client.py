import sys
import alert
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

def client():
    print('Starting PySpark client to process MQTT data stream')

    # Initialize Spark session
    spark = SparkSession.builder.appName("WeatherDataSQL").getOrCreate()

    # Define schema for JSON data
    weatherSchema = StructType([
        StructField("stationId", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("windSpeed", DoubleType(), True),
        StructField("pressure", DoubleType(), True)
    ])

    # Define threshold values
    temperatureThreshold = 25.0
    humidityThreshold = 51.0
    windSpeedThreshold = 51.0
    pressureThreshold = 999.0

    # Connect to the socket server for streaming data
    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Parse JSON strings in incoming data using the predefined schema
    weatherDf = lines.select(from_json(col("value"), weatherSchema).alias("data")).select("data.*")
    # Calculate average for each batch for temperature, humidity, windSpeed, and pressure
    averageDf = weatherDf.groupBy().agg(
        avg("temperature").alias("avgTemperature"),
        avg("humidity").alias("avgHumidity"),
        avg("windSpeed").alias("avgWindSpeed"),
        avg("pressure").alias("avgPressure")
    )

    # Function to process each batch and check thresholds
    def processBatch(df, epochId):
        print(f'Processing batch {epochId}...')

        # Ensure the data types are correct for comparison by casting to DoubleType
        df = df.withColumn("avgTemperature", col("avgTemperature").cast(DoubleType()))
        df = df.withColumn("avgHumidity", col("avgHumidity").cast(DoubleType()))
        df = df.withColumn("avgWindSpeed", col("avgWindSpeed").cast(DoubleType()))
        df = df.withColumn("avgPressure", col("avgPressure").cast(DoubleType()))

        # Fill any missing values (None) with a default value, e.g., 0.0
        df = df.fillna({
            "avgTemperature": 0.0,
            "avgHumidity": 0.0,
            "avgWindSpeed": 0.0,
            "avgPressure": 0.0
        })

        # Collect the DataFrame as a Row object
        avgRow = df.collect()[0]

        avg_temperature = avgRow["avgTemperature"]
        avg_humidity = avgRow["avgHumidity"]
        avg_wind_speed = avgRow["avgWindSpeed"]
        avg_pressure = avgRow["avgPressure"]

        # Perform the comparisons using the thresholds
        if avg_temperature > temperatureThreshold:
            alert.alert(f'High temperature detected: {avg_temperature}°C')
        if avg_humidity > humidityThreshold:
            alert.alert(f'High humidity detected: {avg_humidity}%')
        if avg_wind_speed > windSpeedThreshold:
            alert.alert(f'High wind speed detected: {avg_wind_speed} km/h')
        if avg_pressure < pressureThreshold:
            alert.alert(f'Low pressure detected: {avg_pressure} hPa')


    # Replace lambda with processBatch
    query = averageDf.writeStream \
        .outputMode("complete") \
        .foreachBatch(processBatch) \
        .start()

    # Await termination
    query.awaitTermination()


sys.modules[__name__] = client
