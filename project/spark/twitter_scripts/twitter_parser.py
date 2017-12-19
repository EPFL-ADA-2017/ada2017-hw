'''
The purpose of this script is to fetch the necessary data from 
the Twitter-leon dataset. Below are stated some of the 
assumptions taken throughout the process.

While parsing Twitters string-encoded dates, we ignore the 
time-zone's offset. This is not a problem because:

	1. It avoids the overhead of converting everything into the 
	same timezone
    2. The same day accross all time-zones represents more data
    thatn if we simply considered one (so we are not losing 
    valuable data)
    3. The amount of extra data can be defined as (+/-) 25h 10m,
    which is the largest existing time zone difference in the world
    (between Napari and Samoa)
    4. We can always adjust the time-frame we are considering to
    adjust for these diferences
    5. Since our time-frame is set to 48h, and we ultimately care
    about the contrast on the information before/after a certain 
    date, we will never ignore Tweets that belong to a critical 
    window of (+/-) 22h 50m around the conflict
    6. A critical window of (+/-) 22h 50m around a certain conflict 
    will allow for an overall time-frame of 45h 40m - larger than 
    the largest time-zone difference - which means that regardless 
    of the time of day people might be more active on Twitter, we 
    will always account for their activity
'''

# Add scripts folder to path
import sys
sys.path.append('/home/motagonc/ada2017-hw-private/project/scripts')

# Imports
from pyspark.sql.functions import datediff, unix_timestamp, dayofmonth, year, month, udf
from pyspark.sql.functions import abs as pyspark_abs
from pyspark import SparkContext, SQLContext
from pyspark.sql.types import BooleanType, LongType
from statistics import Statistics
from timer import Timer
from logger import log_print

import language_recognition as lr
import data_handler as dh

# Context initialization
sc = SparkContext()
sqlContext = SQLContext(sc)

# Add modules for UDFs
sc.addPyFile('/home/motagonc/ada2017-hw-private/project/scripts/language_recognition.py')

# Fetch data
log_print('Fetching data from datasets')
twitter_df, ucdp_df = dh.fetch_data('remote', sc)

def filter_twitter_df(twitter_df):
	'''
	This method is used to apply initial filters
	on the Twitter dataframe. It receives the 
	previous dataframe as a parameter and returns 
	a new filtered dataframe.
	'''
	log_print('>> Start >> Filtering Twitter dataframe')

	# Defining necessary UDFs
	is_tweet_english_udf = udf(lr.is_tweet_english, BooleanType())

	# Statistics initialization
	statistics = Statistics('Twitter Filter', False)

	# Removing unnecessary columns
	filtered_twitter_df = twitter_df.drop(twitter_df['User']).drop(twitter_df['ID'])

	# Removing rows with null values (we NEED values for every column)
	filtered_twitter_df = filtered_twitter_df.dropna()

	# Filter english language tweets
	log_print('Filtering \'en\' language entries')
	statistics.set_stage('Pre-defined laguage filter')
	statistics.add_stats('Before', filtered_twitter_df)
	filtered_twitter_df = filtered_twitter_df.filter(filtered_twitter_df['Language'] == 'en').drop(filtered_twitter_df['Language'])
	statistics.add_stats('After', filtered_twitter_df)

	# Parse date format
	log_print('Parsing date format')
	twitter_date_format = "EEE MMM dd HH:mm:ss '+'SSSS yyyy"
	filtered_twitter_df = filtered_twitter_df.withColumn('Timestamp', unix_timestamp(filtered_twitter_df['Date'], twitter_date_format).cast('timestamp')) \
				.drop(filtered_twitter_df['Date'])

	# Filtering English Tweets
	log_print('Filtering english tweets')
	statistics.set_stage('Custom laguage filter')
	statistics.add_stats('Before', filtered_twitter_df)
	filtered_twitter_df = filtered_twitter_df.filter(is_tweet_english_udf(filtered_twitter_df['Content']))
	statistics.add_stats('After', filtered_twitter_df)

	log_print('<<  End  << Filtering Twitter dataframe')

	return (filtered_twitter_df, statistics)

def filter_ucdp_df(ucdp_df):
	'''
	This method is used to apply initial filters
	on the UCDP dataframe. It receives the 
	previous dataframe as a parameter and returns 
	a new filtered dataframe.
	'''
	log_print('>> Start >> Filtering UCDP dataframe')

	# Statistics initialization
	statistics = Statistics('UCDP Filter', False)

	# Parse date format
	log_print('Parsing date format')
	ucdp_date_format = "yyyy-MM-dd"
	filtered_ucdp_df = ucdp_df.withColumn('Timestamp_2', unix_timestamp(ucdp_df['Date Start'], ucdp_date_format).cast('timestamp')) \
				.select('ID', 'Timestamp_2')

	log_print('<<  End  << Filtering UCDP dataframe')

	return (filtered_ucdp_df, statistics)

def merge_dataframes_on_time_window(twitter_df, ucdp_df):
	'''
	This method is used to merge both Twitter
	and UCDP filtered dataframes into a single
	one - based on wether or not a Tweet' timestamp
	is within a certain time window. This can be
	achieved through an inner join.
	'''
	log_print('>> Start >> Filtering on time window')

	# Statistics initialization
	statistics = Statistics('Twitter/UCDP Merging', False)

	# Constants
	DEFAULT_TIME_WINDOW = 2

	# Inner join based on time window
	statistics.set_stage('Custom timestamp filter')
	statistics.add_stats('Before', twitter_df)
	merged_df = twitter_df.join(ucdp_df, (datediff(twitter_df['Timestamp'], ucdp_df['Timestamp_2']) <= DEFAULT_TIME_WINDOW) & (datediff(twitter_df['Timestamp'], ucdp_df['Timestamp_2']) >= -DEFAULT_TIME_WINDOW), 'inner')
	statistics.add_stats('After', merged_df)

	log_print('<<  End  << Filtering on time window')

	return (merged_df, statistics)

# Start overall timer
timer = Timer('Time elapsed')
timer.start()

# Filter dataframes and collect statistics
twitter_df, twitter_statistics = filter_twitter_df(twitter_df)
ucdp_df, ucdp_statistics = filter_ucdp_df(ucdp_df)

# Cache UCDP to speed up merging
ucdp_df.cache()

# Merge dataframes based on time window
merged_df, merged_statistics = merge_dataframes_on_time_window(twitter_df, ucdp_df)

# Print statistics
log_print(twitter_statistics)
log_print(ucdp_statistics)
log_print(merged_statistics)

# Display 5 entries
log_print(twitter_df)
log_print(ucdp_df)
log_print(merged_df)

# save merged results to disk
dh.save_data(merged_df.limit(100), 'motagonc_merged_df_sample')

# Display timer
timer.stop()
log_print(timer)