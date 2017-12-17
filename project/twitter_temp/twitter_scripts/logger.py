from pyspark.sql import DataFrame
from statistics import Statistics
from datetime import datetime

LOG_PRINT_FORMAT = '[{}/{}/{} {}:{}:{}] {} {}'
LOG_LEVELS = ['INFO', 'WARN', 'ERROR']

def _print(message, level):
	current_datetime = datetime.now()
	print(LOG_PRINT_FORMAT.format(
		str(current_datetime.day).zfill(2),
		str(current_datetime.month).zfill(2),
		str(current_datetime.year).zfill(4),
		str(current_datetime.hour).zfill(2),
		str(current_datetime.minute).zfill(2),
		str(current_datetime.second).zfill(2),
		LOG_LEVELS[level].ljust(6),
		message
	))

def log_print(object, level=0):
	if (isinstance(object, DataFrame)):
		_print("Printing dataframe sample", level)
		object.limit(5).show()
	elif (isinstance(object, Statistics)):
		_print("Printing statistics summary", level)
		print(object, level)
	else:
		_print(object, level)