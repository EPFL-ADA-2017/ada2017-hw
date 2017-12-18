# Parsers directory

This directory contains all the notebooks that were used as parsers for our datasets. Hence, their only purpose it to read information from the project's */data/raw* directory and write to */data/parsed* whatever information they find necessary.

Bear in mind that for some datasets, even though there is only one input *raw* file, there can be multiple *parsed* outputs. These are usually to clarify some information and allow more straightforward searching on some components.

This directory represents the 1st step in the data pipeline: 
1. [**parsers**](https://github.com/nunomota/ada2017-hw/tree/master/project/parsers)
2. [analyzers](https://github.com/nunomota/ada2017-hw/tree/master/project/analyzers)
3. [filters](https://github.com/nunomota/ada2017-hw/tree/master/project/filters)