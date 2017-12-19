'''
The Timer class is a simple version of an actual 
timer. When started it stores the starting time 
and when stopped it stores the stopping time.

Both __repr__ and __str__ methods have been
overriden to allow easier and clearer prints.
'''

# Imports
from datetime import datetime, timedelta

class Timer:

    _timer_label = None
    _start_time = None
    _end_time = None

    # Constructor
    def __init__(self, label):
        self._timer_label = label

    '''
    Private Methods
    '''
    def _get_current_time(self):
        '''
        This method returns the current
        time as a datetime object.
        '''
    	return datetime.now()

    def _get_time_delta(self):
        '''
        This method returns the timedelta
        between two datetime objects.
        '''
    	return self._end_time - self._start_time

    '''
    Public Methods
    '''
    def start(self):
        '''
        This method is used to start
        the Timer object.
        '''
        self._start_time = self._get_current_time()

    def stop(self):
        '''
        This method is used to stop
        the Timer object.
        '''
    	self._end_time = self._get_current_time()

    '''
    Methods' Override
    '''
    def __repr__(self):
        '''
        This method overrides the default
        object representation for the Timer
        class' objects.
        '''
        overall_str_format = '{} [{} Days, {} Hours, {} Minutes, {} Seconds]'
        overall_time_delta = self._get_time_delta()

        overall_time_delta_days = overall_time_delta.days
        overall_time_delta_hours, remainder = divmod(overall_time_delta.seconds, 3600)
        overall_time_delta_minutes, overall_time_delta_seconds = divmod(remainder, 60)
        return overall_str_format.format(
        	self._timer_label,
        	overall_time_delta_days,
        	overall_time_delta_hours,
        	overall_time_delta_minutes,
        	overall_time_delta_seconds 
        )

    def __str__(self):
        '''
        This method overrides the default
        object string representation for 
        the Timer class' objects.
        '''
        overall_str_format = '{} [{} Days, {} Hours, {} Minutes, {} Seconds]'
        overall_time_delta = self._get_time_delta()
        
        overall_time_delta_days = overall_time_delta.days
        overall_time_delta_hours, remainder = divmod(overall_time_delta.seconds, 3600)
        overall_time_delta_minutes, overall_time_delta_seconds = divmod(remainder, 60)
        return overall_str_format.format(
        	self._timer_label,
        	overall_time_delta_days,
        	overall_time_delta_hours,
        	overall_time_delta_minutes,
        	overall_time_delta_seconds 
        )