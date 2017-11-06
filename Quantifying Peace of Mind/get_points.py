import findspark
findspark.init()

import pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col

ZIPCODES = pd.read_csv('zipcodes.csv').set_index('ZIP').to_dict('index')

def load_csv(spark, city, year):
    location = '{}/{}.csv'.format(city, year)
    return spark.read.csv(location, header=True)

def main():
    spark = SparkSession.builder.appName("Get Zipcodes").getOrCreate()
    # ZIPCODES = spark.read.csv('zipcodes.csv', header=True)
    dfs = []
    for year in range(2012, 2017):
        df = load_csv(spark, 'nyc', year)
        points = df.selectExpr("cast(unix_timestamp(`Created Date`, 'MM/dd/yyyy hh:mm:ss a') AS timestamp) AS date",
                               "`Complaint Type` AS complaint_type",
                               "cast(`Incident Zip` AS int) AS zipcode").withColumn('city', lit('nyc'))
        dfs.append(points.toPandas())

    for year in range(2011, 2016):
        df = load_csv(spark, 'la', year)
        points = df.selectExpr("cast(unix_timestamp(`Date`, 'MM/dd/yyyy') AS timestamp) AS date",
                               "`Department Name` AS complaint_type",
                               "cast(`Zip Code` AS int) AS zipcode").withColumn('city', lit('la'))
        # pdf = points.selectExpr("dayofyear(date) AS dayofyear",
        #                         "month(date) AS month",
        #                         "year(date) AS year",
        #                         "complaint_type",
        #                         "zipcode")
        # dfs.append(pdf.toPandas())
        # points = points.join(ZIPCODES, points.zipcode == ZIPCODES.ZIP, 'inner')\
        #                .selectExpr("date", "complaint_type", "city", "`LAT` AS lat", "`LNG` AS lng")

        dfs.append(points.toPandas())

    zips = pd.concat(dfs)
    zips.dropna(inplace=True)
    zips['date'] = pd.to_datetime(zips['date'])
    # zips['lat'] = zips['zipcode'].map(lambda z: ZIPCODES[z]['LAT'])
    # zips['lon'] = zips['zipcode'].map(lambda z: ZIPCODES[z]['LNG'])
    zips['month'] = zips['date'].dt.month
    zips['year'] = zips['date'].dt.year
    zips['dayofyear'] = zips['date'].dt.dayofyear

    zips.loc[(zips['year'] >= 2012) & (zips['year'] <= 2015) & (zips['zipcode'].isin(ZIPCODES.keys()))]

    points = zips.drop(['date'], axis=1)

    points.to_csv('points.csv')


if __name__ == '__main__':
    main()

