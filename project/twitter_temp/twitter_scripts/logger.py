from pyspark.sql import DataFrame
from statistics import Statistics
from datetime import datetime

PRINT_RETRY_ATTEMPTS = 3

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

def _show_dataframe(dataframe):
	successfull_print = False
	failed_attempts = 0
	while (failed_attempts < PRINT_RETRY_ATTEMPTS + 1):
		try:
			dataframe.limit(5).show()
		except Exception as exception:
			failed_attempts = failed_attempts + 1
			_print('({}) Failed sample attempt. Retrying [{}/{}]'.format(type(exception).__name__, failed_attempts, PRINT_RETRY_ATTEMPTS), 1)
		else:
			return
	_print('Maximum retry limit exceeded, giving up on action.', 2)

def _show_statistics(statistics):
	if (statistics._is_enabled == True):
		print(statistics)
	else:
		_print('"{}" statistics are DISABLED'.format(statistics._statistics_label), 1)

def log_print(object, level=0):
	if (isinstance(object, DataFrame)):
		_print('Printing dataframe sample', level)
		_show_dataframe(object)
	elif (isinstance(object, Statistics)):
		_print('Printing statistics summary', level)
		_show_statistics(object)
	else:
		_print(object, level)