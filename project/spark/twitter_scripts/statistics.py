'''
This class was created as a container
for statistical information. Each Statistics
object should represent a single operation
and can be internally separated in 'stages'.
'''

class Statistics:

    _statistics_label = None
    _is_enabled = None
    _cur_stage = None
    _data = None

    # Constructor
    def __init__(self, label, enabled):
        self._statistics_label = label
        self._is_enabled = enabled
        self._cur_stage = 'Default'
        self._data = {}

    '''
    Private Methods
    '''
    def _get_dataframe_count(self, dataframe):
        '''
        This method returns the approximate
        number of elements in a dataframe.
        '''
        return dataframe.rdd.countApprox(timeout=1000)

    '''
    Public Methods
    '''
    def set_stage(self, stage_name):
        '''
        This method updates the current
        stage.
        '''
        self._cur_stage = stage_name

    def add_stats(self, label, dataframe):
        '''
        This method adds a certain dataframe's
        statistics to the currently selected
        stage.
        '''
    	if (self._is_enabled == False):
    		return

        stage_data = self._data.get(self._cur_stage, {})
        stage_data[label] = '# Rows: {}'.format(self._get_dataframe_count(dataframe))
        self._data[self._cur_stage] = stage_data

    '''
    Overriden Methods
    '''
    def __repr__(self):
        '''
        This method overrides the default
        object representation for the 
        Statistics class' objects.
        '''
        overall_str_format = '{}: {}'
        return overall_str_format.format(self._statistics_label, list(self._data.keys()))

    def __str__(self):
        '''
        This method overrides the default
        object string representation for 
        the Statistics class' objects.
        '''
        overall_str_format = '---{}---{}\n---------------------'
        stage_str_format = '\n|\n| {}:\n|{}'
        stat_str_format = '\n| \t[{}] {}'

        stage_str = ''
        for stage, stage_data in self._data.iteritems():
            stat_str = ''
            for label, value in stage_data.iteritems():
                stat_str = stat_str + stat_str_format.format(label.ljust(8), value)
            stage_str = stage_str + stage_str_format.format(stage, stat_str)
        return overall_str_format.format(self._statistics_label.ljust(15, '-'), stage_str)