from datetime import datetime, timedelta

class Timer:

    _timer_label = None
    _start_time = None
    _end_time = None

    def __init__(self, label):
        self._timer_label = label

    def _get_current_time(self):
    	return datetime.now()

    def _get_time_delta(self):
    	return self._end_time - self._start_time

    def start(self):
        self._start_time = self._get_current_time()

    def stop(self):
    	self._end_time = self._get_current_time()

    def __repr__(self):
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