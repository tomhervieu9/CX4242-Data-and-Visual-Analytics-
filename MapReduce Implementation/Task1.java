package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Task1 {
//________________________________________________________________
  public static class TokenizerMapper
  	extends Mapper<Object, Text, Text, IntWritable> {
  	private IntWritable weight = new IntWritable();
    private Text tgt = new Text();
    private Text src = new Text();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        src.set(itr.nextToken());
        tgt.set(itr.nextToken());
        weight.set(Integer.parseInt(itr.nextToken()));
        context.write(tgt, weight);
      }
    }
  }  
//________________________________________________________________
  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
        Context context) throws IOException, InterruptedException {
      int max = 0;
      for (IntWritable val : values) {
      	if (val.get() > max) {
        	max = val.get();
    	  }
      }
        result.set(max);
        context.write(key, result);
    }
  }



//________________________________________________________________
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Task1");
    job.setJarByClass(Task1.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }

//________________________________________________________________
}
