# Add scripts folder to path
import sys
sys.path.append('/home/motagonc/ada2017-hw-private/project/scripts')

# Imports
from pyspark.sql.functions import abs, datediff, unix_timestamp, dayofmonth, year, month, udf
from pyspark import SparkContext, SQLContext
from pyspark.sql.types import BooleanType
from statistics import Statistics
from timer import Timer
from logger import log_print

import language_recognition as lr
import data_handler as dh

# context initialization
sc = SparkContext()
sqlContext = SQLContext(sc)

# Add modules for UDFs
sc.addPyFile('/home/motagonc/ada2017-hw-private/project/scripts/language_recognition.py')

# Fetch data
log_print('Fetching data from datasets')
twitter_df, ucdp_df = dh.fetch_data('local', sc)

def filter_twitter_df(twitter_df):

	log_print('>> Start >> Filtering Twitter dataframe')

	# defining necessary UDFs
	is_tweet_english_udf = udf(lr.is_tweet_english, BooleanType())

	# statistics initialization
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

	# Parse date format (avoid UDFs because of serialization/desirialization overhead)
	''' 
	Format ignores the Time-Zone component. This is not a problem for a couple of reasons:

	1. In this case we can increase the parsing/filtering speed of our algorithm
	2. It doesn't really affect our results since it simply will leave more information
	at filtering stage
	3. After filtering, we can define our margin of error as being (+/-) 25h 10m (the largest
	existing time zone difference between Napari and Samoa)
	4. We can always adjust our 'time-frame' to account for these differences
	5. Since our timeframe will always be greater than 48h, and we care mainly about the emotional
	transition from before/after a conflict, regardless of time-zone, we will never ignore Tweets
	that belong to a critical window of (+/-) 22h 50m around the conflict.
	6. A critical window of (+/-) 22h 50m around an event will allow for an overall timeframe
	of 45h 40m, larger than the biggest time-zone difference - so regardless of the time of day people
	might be more active on Twitter, we will always account for their activity 
	'''
	log_print('Parsing date format')
	twitter_date_format = "EEE MMM dd HH:mm:ss '+'SSSS yyyy"
	filtered_twitter_df = filtered_twitter_df.withColumn('Timestamp', unix_timestamp(filtered_twitter_df['Date'], twitter_date_format).cast('timestamp')) \
				.drop(filtered_twitter_df['Date'])

	log_print('Filtering english tweets')
	statistics.set_stage('Custom laguage filter')
	statistics.add_stats('Before', filtered_twitter_df)
	filtered_twitter_df = filtered_twitter_df.filter(is_tweet_english_udf(filtered_twitter_df['Content']))
	statistics.add_stats('After', filtered_twitter_df)

	log_print('<<  End  << Filtering Twitter dataframe')

	return (filtered_twitter_df, statistics)

def filter_ucdp_df(ucdp_df):

	log_print('>> Start >> Filtering Twitter dataframe')

	# statistics initialization
	statistics = Statistics('UCDP Filter', False)

	log_print('Parsing date format')
	ucdp_date_format = "yyyy-MM-dd"
	filtered_ucdp_df = ucdp_df.withColumn('Timestamp', unix_timestamp(ucdp_df['Date Start'], ucdp_date_format).cast('timestamp')) \
				.drop(ucdp_df['Date Start']) \
				.drop(ucdp_df['Date End'])

	log_print('<<  End  << Filtering Twitter dataframe')

	return (filtered_ucdp_df, statistics)

def merge_dataframes_on_time_window(twitter_df, ucdp_df):
	log_print('>> Start >> Filtering on time window')

	# statistics initialization
	statistics = Statistics('Twitter/UCDP Merging', False)

	# constants
	DEFAULT_TIME_WINDOW = 2

	statistics.set_stage('Custom timestamp filter')
	statistics.add_stats('Before', twitter_df)
	merged_df = twitter_df.join(ucdp_df, datediff(twitter_df['Timestamp'], ucdp_df['Timestamp']) <= DEFAULT_TIME_WINDOW, 'inner')
	statistics.add_stats('After', merged_df)

	log_print('<<  End  << Filtering on time window')

	return (merged_df, statistics)

# Start overall timer
timer = Timer('Time elapsed')
timer.start()

# Filter dataframes and collect statistics
twitter_df, twitter_statistics = filter_twitter_df(twitter_df)
ucdp_df, ucdp_statistics = filter_ucdp_df(ucdp_df)

# Merge dataframes based on time window
merged_df, merged_statistics = merge_dataframes_on_time_window(twitter_df, ucdp_df)

# Print statistics
log_print(twitter_statistics)
log_print(ucdp_statistics)

# Display 5 entries
log_print(twitter_df)
log_print(ucdp_df)

ucdp_df.repartition(ucdp_df['Country'])
dh.save_data(ucdp_df, 'motagonc_ucdp_df_sample')

# Display merged results
#log_print(merged_df)
#log_print(merged_statistics)

# Display timer
timer.stop()
log_print(timer)