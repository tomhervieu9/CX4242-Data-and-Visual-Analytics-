package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2"))

    // read the file


    val file = sc.textFile("hdfs://localhost:8020" + args(0))
    /* TODO: Needs to 0, 1be implemented */

	val filter = file.map(seg => 
        seg.split("\t")).filter(seg => (seg(2).toInt != 1))
    val src = filter.map(seg => 
        (seg(0), -1 * seg(2).toInt)).reduceByKey(_+_)
    val tgt = filter.map(seg => 
        (seg(1), 1 * seg(2).toInt)).reduceByKey(_+_)
    val weight = (src union tgt).reduceByKey(_+_)
    val transformation = weight.map(seg => 
        seg._1 + "\t" + seg._2)

    // store output on given HDFS path.
    // YOU NEED TO CHANGE THIS
    transformation.saveAsTextFile("hdfs://localhost:8020" + args(1))
  }
}
