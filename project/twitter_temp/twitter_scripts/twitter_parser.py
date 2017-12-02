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

# Display 5 entries
twitter_df.show(5)