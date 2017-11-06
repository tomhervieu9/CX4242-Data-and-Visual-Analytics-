import findspark
findspark.init()

import pyspark
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

REAL_ESTATE = pd.read_csv('nyc/real_estate.csv')

# def load_year(spark, year):
#     location = "s3://cx4242-311data/nyc/" + str(year) + ".csv"
#     return spark.read.csv(location, header=True)
def load_year(spark, year):
    location = "nyc/{}.csv".format(year)
    return spark.read.csv(location, header=True)

def clean_df(df):
    return df.selectExpr("cast(unix_timestamp(`Created Date`, 'MM/dd/yyyy hh:mm:ss a') AS timestamp) AS created_date",
                         "cast(unix_timestamp(`Closed Date`, 'MM/dd/yyyy hh:mm:ss a') AS timestamp) AS closed_date",
                         "`Complaint Type` AS complaint_type",
                         "`Descriptor` AS descriptor",
                         "cast(`Incident Zip` AS int) AS zipcode")

def get_features(sparkdf, complaint_column, year):
    df = sparkdf.groupby('zipcode').pivot(complaint_column).count().toPandas().fillna(0)
    # import ipdb; ipdb.set_trace()
    features = df.merge(REAL_ESTATE.loc[:, ['zipcode', str(year)]], on='zipcode').rename(columns={str(year): 'price'})
    return features.dropna(subset=['zipcode', 'price']).set_index('zipcode')
    

# def write_df(df, name):
#     df.write.csv("s3://cx4242-311data/" + name + ".csv", header=True)
def write_df(df, name):
    df.to_csv("nyc/{}.csv".format(name))

def dump_zipcodes(features):
    """Simple utility function to write all zipcodes in nyc to a file so real estate data for them can be downloaded."""
    zipcodes = features["zipcode"]
    zipcodes.to_csv("nyc-zipcodes.csv")


def main():
    spark = SparkSession.builder.appName("Spark NYC ETL").getOrCreate()
    for year in range(2012,2017):
        df = clean_df(load_year(spark, year)).filter(F.col("zipcode").isNotNull() & F.col("complaint_type").isNotNull())
        # valid zipcodes are 5 digit numbers
        df = df.filter((df['zipcode'] >= 10000) & (df['zipcode'] <= 99999))
        df_detailed = df.filter(F.col("descriptor").isNotNull()).selectExpr("zipcode", "CONCAT(TRIM(complaint_type), ':', TRIM(descriptor)) AS detailed_complaint")

        features = get_features(df, 'complaint_type', year)
        features_detailed = get_features(df_detailed, 'detailed_complaint', year)

        write_df(features, str(year) + "-summarized")
        write_df(features_detailed, str(year) + "-detailed-summarized")

def get_all_zipcodes():
    spark = SparkSession.builder.appName("ZIP Codes").getOrCreate()
    df = clean_df(load_year(spark,2012)).filter(F.col("zipcode").isNotNull() & F.col("complaint_type").isNotNull())
    df = df.filter((df['zipcode'] >= 10000) & (df['zipcode'] <= 99999))
    zipcodes = df.select('zipcode').toPandas()['zipcode'].unique()
    np.savetxt("nyc-zipcodes.txt", zipcodes)

if __name__ == '__main__':
    main()
