import codecs
import gzip
from pyspark import SparkContext

DATA_PATH_LOCAL_TWITTER = '/home/motagonc/ada2017-hw-private/project/twitter_temp/twitter_dataset/small_tweet_dataset'
DATA_PATH_LOCAL_UCDP = '/home/motagonc/ada2017-hw-private/project/data/parsed/parsed_ucdp.csv'
DATA_PATH_REMOTE = 'hdfs:////datasets/tweets-leon'

twitter_schema = [
	'Language',
	'ID',
	'Date',
	'User',
	'Content'
]

ucdp_schema = [
	'ID',
	'Year',
	'Type',
	'Conflict Name',
	'Date Start',
	'Date End',
	'Casualties',
	'Country'
]

'''
PRIVATE METHODS
'''

def _fetch_data_failed(spark_context):
	return None

def _fetch_ucdp_data_from_local(spark_context):
	with gzip.open(DATA_PATH_LOCAL_UCDP) as local_file:
		conflicts = [conflict.strip() for conflict in codecs.iterdecode(local_file, 'utf8')][1:]
	return spark_context.parallelize(conflicts)

def _fetch_twitter_data_from_local(spark_context):
	with open(DATA_PATH_LOCAL_TWITTER, 'r') as local_file:
		tweets = local_file.readlines()
	tweets = [tweet.strip() for tweet in tweets]
	return spark_context.parallelize(tweets)

def _fetch_twitter_data_from_remote(spark_context):
	return spark_context.textFile(DATA_PATH_REMOTE)

def _convert_rdd_to_df(target_rdd, split_character, schema):
	split_target_rdd = target_rdd.map(lambda x: x.split(split_character))
	split_target_rdd = split_target_rdd.filter(lambda x: len(x) == len(schema))
	return split_target_rdd.toDF(schema)

'''
PUBLIC METHODS
'''

def download_data_sample(n_entries, spark_context):
	twitter_sample_rows = _fetch_data_from_remote(spark_context).take(n_entries)
	with open(DATA_PATH_LOCAL_TWITTER, 'w') as local_file:
		for sample in twitter_sample_rows:
			encoded_sample = sample.encode('utf-8')
			local_file.write(encoded_sample + '\n')
	return

def fetch_data(source, spark_context):
	twitter_result_rdd = {
		'local': _fetch_twitter_data_from_local,
		'remote': _fetch_twitter_data_from_remote
	}.get(source, _fetch_data_failed)(spark_context)
	
	ucdp_result_rdd = {
		'local': _fetch_ucdp_data_from_local,
		'remote': _fetch_ucdp_data_from_local
	}.get(source, _fetch_data_failed)(spark_context)

	if (twitter_result_rdd is None or ucdp_result_rdd is None):
		return None

	twitter_result_df = _convert_rdd_to_df(twitter_result_rdd, '\t', twitter_schema)
	ucdp_result_df = _convert_rdd_to_df(ucdp_result_rdd, ',', ucdp_schema)

	return (twitter_result_df, ucdp_result_df)

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
