hadoop jar ./target/task4-1.0.jar edu.gatech.cse6242.Task4 /user/cse6242/small.tsv /user/cse6242/task4output1
hadoop fs -getmerge /user/cse6242/task4output1/ task4output1.tsv
hadoop fs -rm -r /user/cse6242/task4output1
