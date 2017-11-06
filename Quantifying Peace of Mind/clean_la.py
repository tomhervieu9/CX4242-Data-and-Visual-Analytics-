import findspark
findspark.init()

import pyspark
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

REAL_ESTATE = pd.read_csv('la/real_estate.csv')

def load_year(spark, year):
    location = 'la/{}.csv'.format(year)
    return spark.read.csv(location, header=True)

def clean_df(df):
    return df.selectExpr("cast(unix_timestamp(`Date`, 'MM/dd/yyyy') AS timestamp) AS date",
                         "`Department Name` AS department",
                         "`Service Name` AS service",
                         "cast(`Zip Code` AS int) AS zipcode")

def get_features(sparkdf, pivot_column, year):
    df = sparkdf.groupby('zipcode').pivot(pivot_column).count().toPandas().fillna(0)
    features = df.merge(REAL_ESTATE.loc[:, ['zipcode', str(year)]], on='zipcode').rename(columns={str(year): 'price'})
    # import ipdb; ipdb.set_trace()
    return features.dropna(subset=['zipcode', 'price']).set_index('zipcode')

def write_df(df, name):
    df.to_csv("la/{}.csv".format(name))


def main():
    spark = SparkSession.builder.appName("Spark LA ETL").getOrCreate()
    for year in range(2011, 2016):
        df = clean_df(load_year(spark, year)).filter(F.col("zipcode").isNotNull())

        df = df.filter((df['zipcode'] >= 10000) & (df['zipcode'] <= 99999))
        features_department = get_features(df.filter(df['department'].isNotNull()), 'department', year)
        features_service = get_features(df.filter(df['service'].isNotNull()), 'service', year)

        write_df(features_department, str(year) + "-summarized")
        write_df(features_service, str(year) + "-detailed-summarized")

def get_all_zipcodes():
    spark = SparkSession.builder.appName("Zip Codes - LA").getOrCreate()
    df = clean_df(load_year(spark, 2011)).filter(F.col("zipcode").isNotNull())
    df = df.filter((df['zipcode'] >= 10000) & (df['zipcode'] <= 99999))

    zipcodes = df.select('zipcode').toPandas()['zipcode'].unique()
    np.savetxt('la-zipcodes.txt', zipcodes, fmt='%d')

if __name__ == '__main__':
    # get_all_zipcodes()
    main()
