'''
This module is used as the interface between the
twitter/ucdp filtering/parsing script and data.
Dependeing on the parameters specified, this code
can provide access to either a local sample of the
data or directly a reference to the remote one.

We tried several approaches to getting the data as
fast as we could. Below is the cleanest way to get
the data from a csv/tsv text file but, sadly, proved
to be really lacking in performance:

	from pyspark.sql.types import StructType, StructField, StringType, IntegerType

	schema = StructType([
		StructField('Language', StringType()),
		StructField('ID', IntegerType()),
		StructField('Date', StringType()),
		StructField('User', StringType()),
		StructField('Content', StringType())
	])

	# Load data into DataFrame
	twitter_df = sqlContext.read.format('com.databricks.spark.csv')
		.option('header', False)
		.option('delimiter', '\t')
		.option('mode', 'DROPMALFORMED')
		.schema(schema)
		.load('hdfs:////datasets/tweets-leon')

On the actual implementation you will notice that
getting an RDD, iterating over the lines, splitting
them, parallelizing them and then converting them to
a DataFrame is quite more performant.
'''

# Imports
import codecs
import gzip
import os, shutil

from pyspark import SparkContext
from logger import log_print

# Cnstants
DATA_PATH_LOCAL_TWITTER = '/home/motagonc/ada2017-hw-private/project/twitter_temp/twitter_dataset/small_tweet_dataset'
DATA_PATH_LOCAL_UCDP = '/home/motagonc/ada2017-hw-private/project/data/parsed/parsed_ucdp.csv'
DATA_PATH_REMOTE = 'hdfs:////datasets/tweets-leon'

DATA_PATH_LOCAL_STORAGE_FORMAT = '/buffer/{}'
DATA_PATH_LOCAL_STORAGE_SPARK_FORMAT = 'file:///{}'
SAVE_RETRY_ATTEMPTS = 3

# Dataframe schemas
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
	'''
	This function gets executed if the data 
	handler fails to fetch the required data 
	(either local or remote).
	'''
	return None

def _fetch_ucdp_data_from_local(spark_context):
	'''
	This function fetches UCDP dataset's local
	data. The returned value is an RDD.
	'''
	with gzip.open(DATA_PATH_LOCAL_UCDP) as local_file:
		conflicts = [conflict.strip() for conflict in codecs.iterdecode(local_file, 'utf8')][1:]
	return spark_context.parallelize(conflicts)

def _fetch_twitter_data_from_local(spark_context):
	'''
	This function fetches Twitter dataset's local
	sampled data. The returned value is an RDD.
	'''
	with open(DATA_PATH_LOCAL_TWITTER, 'r') as local_file:
		tweets = local_file.readlines()
	tweets = [tweet.strip() for tweet in tweets]
	return spark_context.parallelize(tweets)

def _fetch_twitter_data_from_remote(spark_context):
	'''
	This function fetches Twitter dataset's remote
	data. The returned value is an RDD.
	'''
	return spark_context.textFile(DATA_PATH_REMOTE)

def _convert_rdd_to_df(target_rdd, split_character, schema):
	'''
	This function is used to convert RDD with single
	string element rows into a DatFrame. The split
	character defines which character to use when
	splitting the full row, whereas schema provides
	the necessary column-based indexing.
	'''
	split_target_rdd = target_rdd.map(lambda x: x.split(split_character))
	split_target_rdd = split_target_rdd.filter(lambda x: len(x) == len(schema))
	return split_target_rdd.toDF(schema)

'''
PUBLIC METHODS
'''
def download_data_sample(n_entries, spark_context):
	'''
	This function is used to fetch a sample of the
	Twitter's remote dataset. It then stores it in
	a local file.
	'''
	twitter_sample_rows = _fetch_twitter_data_from_remote(spark_context).take(n_entries)
	with open(DATA_PATH_LOCAL_TWITTER, 'w') as local_file:
		for sample in twitter_sample_rows:
			encoded_sample = sample.encode('utf-8')
			local_file.write(encoded_sample + '\n')
	return

def fetch_data(source, spark_context):
	'''
	This function is usedd to fetch the necessary
	data for both Twitter and UCDP datasets. The
	user can specify whether he was to access the
	local sampled versions of the datasets or the
	remote ones. The returned value will be a tuple
	of two dataframes.
	'''
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

def save_data(dataframe, file_name):
	'''
	This function saves a dataframe onto a local
	file, in a default directory. Shall Spark's
	action fail to execute, it will retry it at 
	most 3 times.
	'''
	failed_attempts = 0
	last_exception = None
	save_file_path = DATA_PATH_LOCAL_STORAGE_FORMAT.format(file_name)
	while (failed_attempts < SAVE_RETRY_ATTEMPTS):
		try:
			if (os.path.exists(save_file_path)):
				log_print('"{}" already exists'.format(save_file_path), 1)
				if (os.path.isdir(save_file_path)):
					log_print('Deleting directory: {}'.format(save_file_path), 1)
					shutil.rmtree(save_file_path)
				else:
					log_print('Deleting file: {}'.format(save_file_path), 1)
					os.remove(save_file_path)
			log_print('Writing dataframe to file: {}'.format(save_file_path))
			dataframe.write.format('com.databricks.spark.csv').option('header', 'false').save(DATA_PATH_LOCAL_STORAGE_SPARK_FORMAT.format(save_file_path))
		except Exception as exception:
			failed_attempts = failed_attempts + 1
			last_exception = exception
			log_print('({}) Failed saving attempt. Retrying [{}/{}]'.format(type(exception).__name__, failed_attempts, SAVE_RETRY_ATTEMPTS), 1)
		else:
			return
	print(last_exception)
	log_print('Maximum retry limit exceeded, giving up on action.', 2)