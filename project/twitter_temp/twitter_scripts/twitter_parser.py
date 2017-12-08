from pyspark.sql.functions import unix_timestamp, dayofmonth, year, month
from pyspark import SparkContext, SQLContext
from logger import log_print

import data_handler as dh

# context initialization
sc = SparkContext()
sqlContext = SQLContext(sc)

# Fetch data
log_print('Fetching data from local dataset')
twitter_df = dh.fetch_data('local', sc)

# Filter english language tweets
log_print('Filtering \'en\' language entries')
twitter_df = twitter_df.filter(twitter_df['Language'] == 'en')

# Parse date format (avoid UDFs because of serialization/desirialization overhead)
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

# Display 5 entries
twitter_df.show(5)