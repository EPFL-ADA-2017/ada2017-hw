import codecs
from pyspark import SparkContext

DATA_PATH_LOCAL = '/home/motagonc/twitter_dataset/small_tweet_dataset'
DATA_PATH_REMOTE = 'hdfs:////datasets/tweets-leon'

twitter_schema = [
	'Language',
	'ID',
	'Date',
	'User',
	'Content'
]

'''
PRIVATE METHODS
'''

def _fetch_data_failed(spark_context):
	return None

def _fetch_data_from_local(spark_context):
	with open(DATA_PATH_LOCAL, 'r') as local_file:
		tweets = local_file.readlines()
	tweets = [tweet.strip() for tweet in tweets]
	return spark_context.parallelize(tweets)

def _fetch_data_from_remote(spark_context):
	return spark_context.textFile(DATA_PATH_REMOTE)

def _convert_rdd_to_df(target_rdd):
	split_target_rdd = target_rdd.map(lambda x: x.split('\t'))
	return split_target_rdd.toDF(twitter_schema)

'''
PUBLIC METHODS
'''

def download_data_sample(n_entries, spark_context):
	twitter_sample_rows = _fetch_data_from_remote(spark_context).take(n_entries)
	with open(DATA_PATH_LOCAL, 'w') as local_file:
		for sample in twitter_sample_rows:
			encoded_sample = sample.encode('utf-8')
			local_file.write(encoded_sample + '\n')
	return

def fetch_data(source, spark_context):
	result_rdd = {
		'local': _fetch_data_from_local,
		'remote': _fetch_data_from_remote
	}.get(source, _fetch_data_failed)(spark_context)
	
	if (result_rdd is not None):
		return _convert_rdd_to_df(result_rdd)

	return None

'''
For documentation purposes, this approach is A LOT slower (even though it's clearer):

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
	StructField('Language', StringType()),
	StructField('ID', IntegerType()),
	StructField('Date', StringType()),
	StructField('User', StringType()),
	StructField('Content', StringType())
])

# Load data into DataFrame
twitter_df = sqlContext.read.format('com.databricks.spark.csv').option('header', False).option('delimiter', '\t').option('mode', 'DROPMALFORMED').schema(schema).load('hdfs:////datasets/tweets-leon')

twitter_df.limit(5).show()
'''