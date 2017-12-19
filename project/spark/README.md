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

## Purpose

### 1. First thoughts
Our initial plan was to use the larger Twitter dataset, 'twitter-leon', along with a pre-processed UCDP dataset. Our rudimentary approach was quite straightforward:

1. Initially parsing the Twitter dataset
	* Read the dataset into a Spark DataFrame
	* Filter only the Tweets tagged with 'en'
	* Apply our own language recognition module to further narrow down English Tweets
	* Select only the necessary columns ('Content' and 'Date')
	* Convert StringType Date column into a timestamp (also renaming it to 'Timestamp')

2. Initially parsing the UCDP dataset
	* Read the dataset into a Spark DataFrame
	* Select only the necessary columns ('ID', 'Start Date' and 'Country')
	* Convert StringType Date column into a timestamp (also renaming it to 'Timestamp')

3. Getting the Tweets within 2 days of each conflict:
	* We would now do an inner join on the 'Timestamp'columns 
	* As a condition for the join, instead of equality, we wanted to use 'pyspark.sql.functions.datediff' less or equal than 2
	* Then, drop the unnecessary 'Timestamp' column remaining from the UCDP dataset (we only want the Tweet's timestamp from this point on)

4. Filtering 'interesting' tweets within time span:
	* Using our NER-based module, we would filter down the Dataframe even more based on 'ner.is_tweet_about_country' - applied to both 'Content' and 'Country' columns
	* Since we basically had Tweet/Conflict pairs in the dataframe, now we would have TweetTalkingAboutConflict/Conflict

5. Applying sentiment analysis on Tweets:
	* On the remaining Tweets, we could use our sentiment analysis module - to create a new column 'Sentiment Strength'
	* This new column is a value from -1.0 to 1.0, representing the negativity/positivity of the text

6. Studying the Tweets over time for each conflict:
	* Now the schema for the obtained DataFrame would be ['Content', 'ID', 'Timestamp', 'Country', 'Sentiment Strength']
	* We could separate these entries by 'ID' and group them by 'pyspark.sql.functions.dayofmonth' - on the 'Timestamp' column
	* We could now study the daily sentiment strength, for each conflict, and define 'sentimental impact' on their growth

### 2. Course of action:
This time-line was slowly developed first with our Markov-Chains Tweet generator and then with a tiny sample of the twitter-leon dataset.

#### 2.1. Markov-Chain generator:
In the first stage, since we could create the Tweets ourselves, we always generated Tweets already within 2 days of each conflict (and a few random others). Although a good in-house proof of concept, they are not real tweets and so we can't take any conclusions from the results we get. We can simply test our 'daily sentiment strength' calculations and the 'stentimental impact'.

#### 2.2. Sampling Twitter-leon:
When we moved to getting a sample from the Twitter dataset we found our first obstacle: sampling the dataframe on the Timestamp column would simply take too long. Hence, we simply opted to generate a local dataset with random entries (rdd.take(n)) - which was way faster. Since we had no control over the dates we sampled, we picked conflicts that would align with some of the Tweets we got. It was better than using the Markov-Chain generator but since many of these conflicts were quite fleeting or small, again, we couldn't take any conclusions from our results (just allowing us to further develop our methodology to eventually apply on the whole dataset).

#### 2.3. The Spark brick wall:
Everything seemed well thought and implemented so we decided to give it a go with the remote dataset directly. From lengthy runs ending in a closed SparkContext (due to java.lang.OutOfMemoryError) to sucessfull runs failing the 'saveToTextFile' job (the necessary one...), it was a lot of work to try and figure out how to better fetch our data. Here are the things we took into consideration:

1. Filter down the data as much as possible
	* This should allow some actions to run faster

2. Never trust order
	* Automatic reshuffling can be your enemy

3. Only use Actions when strictly necessary
	* The only Action we are performing, as of now, is the 'saveToTextFile' at the end

4. Avoid UDFs as much as possible
	* Since serialization/deserialization required to work with Python introduces a big operational overhead
	* We ended up removing the sentiment analysis and the name entity recognition steps from the Spark-dependent pipeline
	* All UDFs (except for the language recognition one) were to be used as normal functions after getting the filtered data
	* This would mean we couldn't initially filter Tweets as well but time-wise it should be faster to just: 'dataframe.limit(n)'; save to a file; read the data (e.g. with pandas); and apply our local functions.
	* All the functions used for filtering where taken from 'pyspark.sql.functions'

5. Persist dataframes that would be needed for several operations
	* We didn't persist the Twitter dataframe due to the amount of data but we did with the UDCP one - to hopefully reduce the inner join's running time

### 3. End Result
Regardless of this, we couldn't find a solution that would run in a time-efficient way so we had to pivot the aim of our project. Regardless, here are some steps we think could have made it possible in case we kept on that path:

1. Use column-oriented data formats (such as Parquet or ORC) to store intermediate datasets
2. Directly use Scala/Java on Spark's client side
3. Implement our UDFs in Scala/Java and exporting them as 'jars' (to prevent serialization/deserialization when executing them on the JVM)
4. Study a way to correctly partition our data based on the available resources
5. Find fastest approaches to our problem ('RDD vs DataFrame' or 'SQL vs Methods') since some approaches seem to be better optimized, in the background