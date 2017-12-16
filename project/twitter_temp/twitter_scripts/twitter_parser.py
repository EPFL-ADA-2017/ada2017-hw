# Add scripts folder to path
import sys
sys.path.append('/home/motagonc/ada2017-hw-private/project/scripts')

# Imports
from pyspark.sql.functions import unix_timestamp, dayofmonth, year, month, udf
from pyspark import SparkContext, SQLContext
from pyspark.sql.types import BooleanType
from statistics import Statistics
from logger import log_print

import language_recognition as lr
import data_handler as dh

# context initialization
sc = SparkContext()
sqlContext = SQLContext(sc)

# Add modules for UDFs
sc.addPyFile('/home/motagonc/ada2017-hw-private/project/scripts/language_recognition.py')

# statistics initialization
statistics = Statistics('Twitter Filter', True)

# Fetch data
log_print('Fetching data from local dataset')
twitter_df, ucdp_df = dh.fetch_data('local', sc)

# Removing unnecessary columns
twitter_df = twitter_df.drop(twitter_df['User']).drop(twitter_df['ID'])

# Removing rows with null values (we NEED values for every column)
twitter_df = twitter_df.dropna()

# Filter english language tweets
log_print('Filtering \'en\' language entries')
statistics.set_stage('Pre-defined laguage filter')

statistics.add_stats('Before', twitter_df)
twitter_df = twitter_df.filter(twitter_df['Language'] == 'en').drop(twitter_df['Language'])
statistics.add_stats('After', twitter_df)

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
date_format = "EEE MMM dd HH:mm:ss '+'SSSS yyyy"
twitter_df = twitter_df.withColumn('Timestamp', unix_timestamp(twitter_df['Date'], date_format).cast('timestamp')) \
			.drop(twitter_df['Date'])
'''
log_print('Separating date into \'day\', \'month\' and \'year\' columns')
twitter_df = twitter_df.withColumn('Day', dayofmonth(twitter_df['Parsed Date']).cast('string')) \
			.withColumn('Month', month(twitter_df['Parsed Date']).cast('string')) \
			.withColumn('Year', year(twitter_df['Parsed Date']).cast('string')) \
			.drop(twitter_df['Parsed Date'])
'''

log_print('Filtering english tweets')
statistics.set_stage('Custom laguage filter')
is_tweet_english_udf = udf(lr.is_tweet_english, BooleanType())

statistics.add_stats('Before', twitter_df)
twitter_df = twitter_df.filter(is_tweet_english_udf(twitter_df['Content']))
statistics.add_stats('After', twitter_df)

# Print statistics
print(statistics)

# Display 5 entries
twitter_df.show(5)