'''
The logger is a simple set of functions to
allow easier and clearer logging of our scripts.
This will generate labeled, aligned and formatted
printed lines - ideally always used instead of 
regular prints.
'''

# Imports
from pyspark.sql import DataFrame
from statistics import Statistics
from datetime import datetime

# Constants
PRINT_RETRY_ATTEMPTS = 3

LOG_PRINT_FORMAT = '[{}/{}/{} {}:{}:{}] {} {}'
LOG_LEVELS = ['INFO', 'WARN', 'ERROR']


'''
Private Functions
'''
def _print(message, level):
	'''
	This functions directly formats and prints
	a certain message with a priority level and
	the correspondant timestamp.
	'''
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
	'''
	This functions is called specifically
	for DataFrames' representation. It avoids
	weird formatting and action failure. If
	the later happens, it retries up to 3 
	times.
	'''
	failed_attempts = 0
	last_exception = None
	while (failed_attempts < PRINT_RETRY_ATTEMPTS):
		try:
			dataframe.limit(5).show()
		except Exception as exception:
			failed_attempts = failed_attempts + 1
			last_exception = exception
			_print('({}) Failed sample attempt. Retrying [{}/{}]'.format(type(exception).__name__, failed_attempts, PRINT_RETRY_ATTEMPTS), 1)
		else:
			return
	print(last_exception)
	_print('Maximum retry limit exceeded, giving up on action.', 2)

def _show_statistics(statistics):
	'''
	This function is called specifically 
	for Statistics' representation. It avoids
	unnecessary empty prints for disabled 
	objects (simply warning the user instead).
	'''
	if (statistics._is_enabled == True):
		print(statistics)
	else:
		_print('"{}" statistics are DISABLED'.format(statistics._statistics_label), 1)

'''
Public Functions
'''
def log_print(object, level=0):
	'''
	This function is called from within many
	other modules, providing an easy way to
	generate logging-friendly prints.
	'''
	if (isinstance(object, DataFrame)):
		_print('Printing dataframe sample', level)
		_show_dataframe(object)
	elif (isinstance(object, Statistics)):
		_print('Printing statistics summary', level)
		_show_statistics(object)
	else:
		_print(object, level)