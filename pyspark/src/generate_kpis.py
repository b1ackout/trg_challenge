#!/usr/bin/python

import pyspark

from config import kpis

if __name__ == '__main__':
    sc = pyspark.SparkContext(appName="Challenge2")

    try:
        spark = pyspark.sql.SparkSession(sc)
        spark.read.parquet('file:///data/crimes').registerTempTable('crimes')

        for kpi in kpis:
            spark.sql(kpi['query']) \
                .repartition(1) \
                .write \
                .mode('overwrite') \
                .json(f'file:///data/kpis/{kpi["name"]}')
        print(f'KPI files were successfully generated')
    finally:
        sc.stop()
