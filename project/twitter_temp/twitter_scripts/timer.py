from datetime import datetime, timedelta

class Timer:

    _timer_label = None
    _start_time = None
    _end_time = None

    def __init__(self, label):
        self._timer_label = label

    def _get_current_time():
    	return datetime.now()

    def _get_time_delta():
    	return self._end_time - self._start_time

    def start(self):
        self._start_time = _get_current_time()

    def stop(self):
    	self._end_time = _get_current_time()

    def __repr__(self):
        overall_str_format = '[{}] {} Days : {} Hours : {} Minutes : {} Seconds'
        overall_time_delta = _get_time_delta()
        return overall_str_format.format(
        	self._timer_label,
        	overall_time_delta.days,
        	overall_time_delta.hours,
        	overall_time_delta.minutes,
        	overall_time_delta.seconds 
        )

    def __str__(self):
        overall_str_format = '[{}] {} Days : {} Hours : {} Minutes : {} Seconds'
        overall_time_delta = _get_time_delta()
        return overall_str_format.format(
        	self._timer_label,
        	overall_time_delta.days,
        	overall_time_delta.hours,
        	overall_time_delta.minutes,
        	overall_time_delta.seconds 
        )