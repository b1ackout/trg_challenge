#!/usr/bin/python

import pyspark
from pyspark.sql.functions import input_file_name, last, col
from pyspark.sql.window import Window

from config import extract_file_name_udf

if __name__ == '__main__':
    sc = pyspark.SparkContext(appName="Challenge1")

    try:
        spark = pyspark.sql.SparkSession(sc)

        spark.read.csv('file:///data/crimes_csv/*/*-street.csv', header=True) \
            .where('`Crime ID` is not null') \
            .withColumn("districtName", extract_file_name_udf(input_file_name())) \
            .selectExpr('`Crime ID` as crimeId','latitude', 'longitude', '`Crime type` as crimeType', 
                        '`Last outcome category` as lastOutcomeCategory', 'Month as Month',
                        'districtName') \
            .dropDuplicates() \
            .registerTempTable('s')

        spark.read.csv('file:///data/crimes_csv/*/*-outcomes.csv', header=True) \
            .where('`Crime ID` is not null') \
            .selectExpr('`Crime ID` as crimeId','latitude', 'longitude', '`Outcome type` as lastOutcome', 'Month') \
            .withColumn('lastOutcome', last('lastOutcome', True).over(
                    Window.partitionBy("crimeId").orderBy(col("month")))) \
            .dropDuplicates() \
            .groupBy('crimeId').agg(last('lastOutcome', True).alias('lastOutcome')) \
            .registerTempTable('o')

        spark.sql('''SELECT s.crimeId, 
                            Month, 
                            districtName, 
                            s.latitude, 
                            s.longitude, 
                            s.crimeType, 
                            nvl(lastOutcome, lastOutcomeCategory) AS lastOutcome 
                    FROM s LEFT JOIN o 
                        ON s.crimeId = o.crimeId''') \
                .write.mode('overwrite') \
                .partitionBy('month') \
                .parquet('/data/crimes')
        print(f'Crimes files were successfully generated')
    finally:
        sc.stop()
