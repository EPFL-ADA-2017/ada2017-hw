class Statistics:

    _statistics_label = None
    _is_enabled = None
    _cur_stage = None
    _data = None

    def __init__(self, label, enabled):
        self._statistics_label = label
        self._is_enabled = enabled
        self._cur_stage = 'Default'
        self._data = {}

    def set_stage(self, stage_name):
        self._cur_stage = stage_name

    def add_stats(self, label, dataframe):
    	if (self._is_enabled == False):
    		return

        stage_data = self._data.get(self._cur_stage, {})
        stage_data[label] = '# Rows: {}'.format(self._get_dataframe_count(dataframe))
        self._data[self._cur_stage] = stage_data

    def _get_dataframe_count(self, dataframe):
        return dataframe.rdd.countApprox(timeout=1000)

    def __repr__(self):
        overall_str_format = '{}: {}'
        return overall_str_format.format(self._statistics_label, list(self._data.keys()))

    def __str__(self):
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