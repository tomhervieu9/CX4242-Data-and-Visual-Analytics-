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
import org.apache.hadoop.fs.FileSystem;

public class Task4 {
//________________________________________________________________
  public static class TokenizerMapper
  	extends Mapper<Object, Text, Text, IntWritable> {
    private Text tgt = new Text();
    private Text src = new Text();
    private IntWritable one = new IntWritable(1);

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        src.set(itr.nextToken());
        tgt.set(itr.nextToken());
        context.write(src,one);
        context.write(tgt,one);
      }
    }
  }  
//________________________________________________________________
  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
        Context context) throws IOException, InterruptedException {
      int count = 0;
      for (IntWritable val : values) {
      	count += 1;
      }
        result.set(count);
        context.write(key, result);
    }
  }

//________________________________________________________________
  public static class TokenizerMapper2
  	extends Mapper<Object, Text, Text, IntWritable> {
    private Text deg= new Text();
    private Text freq = new Text();
    private IntWritable one = new IntWritable(1);

    public void map(Object key, IntWritable value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        deg.set(itr.nextToken());
        freq.set(itr.nextToken());
        context.write(deg,one);
      }
    }
  }  
//________________________________________________________________
  public static class IntSumReducer2
       extends Reducer<Text,IntWritable,Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
        Context context) throws IOException, InterruptedException {
      int count = 0;
      for (IntWritable val : values) {
      	count += 1;
      }
        result.set(count);
        context.write(key, result);
    }
  }


//________________________________________________________________
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Task4");
    Job job2 = Job.getInstance(conf, "Task4");
    FileSystem system = FileSystem.get(new Configuration());
    system.delete(new Path("/user/cse6242/temp1"), true);
    system.delete(new Path(args[1]), true);


    job.setJarByClass(Task4.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("/user/cse6242/temp1"));
    job.waitForCompletion(true);

    job2.setJarByClass(Task4.class);
    job2.setMapperClass(TokenizerMapper2.class);
    job2.setCombinerClass(IntSumReducer2.class);
    job2.setReducerClass(IntSumReducer2.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job2, new Path("/user/cse6242/temp1"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }

//________________________________________________________________
}
