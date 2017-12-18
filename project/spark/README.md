# Spark directory
In this directory you will find all of the files associated with our attempt at getting the data from the cluster (from the twitter-leon dataset). You can experiment with them as juch as you'd like but bear in mind you will have to change the directories defined in the beginning of some of the scripts (since, to avoid move problems down the line when re-organizing the project, the defined paths to some of the resources are absolute - not relative). Same applies to the user inside of the [status script](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/status) - you will have to change it to your own username.

## Usage
The python file that contains all the code for parsing/filtering the information we want is the [twitter_parser.py](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/twitter_scripts/twitter_parser.py). To submit it from within the cluster, you just have to run `./submit twitter_scripts/twitter_parser.py`. To submit from your own machine, please mind the TAs' notes on how to steup Spark.

## Submit script
This script needs one argument in order to be executed - the path to your python script. Inside, it basically calls `spark-submit` with all the necessary parameters, including resource allocation, and `screen`, to run your process detached from your SSH session. Feel free to exit your session - the process will still keep executing while you are not connected.

**Note:** The script also redirects all the output to files inside the *logs* directory - *script_output.log* and *spark_output.log*.

## Status script
Since the [submit script](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/submit) runs the process in detached mode and all the output gets redirected into files, this script provides an easy way to check whether or not your process, `screen`, is still running. After you run `./status`, you will either see `Running` or `Stopped`. You can then refer to the *logs* directory in order to find the results of your submission.

## twitter_scripts directory
Contains both the [twitter_parser.py](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/twitter_scripts/twitter_parser.py), in charge of all the data-wise heavy-lifting, and all its auxiliary scripts.

## twitter_dataset directory
This directory simply contains a small sample of the Twitter-leon dataframe.