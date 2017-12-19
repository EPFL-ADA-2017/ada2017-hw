# Sentimental impact of world events on the Twitter social netwrok

## Abstract

The aim of our project is to quantify the *sentimental impact* of a certain world event, on the Twitter community. 

In order to reach this goal we used the UCDP dataset, to focus on events (in this case conflicts) that would most likely raise international concern, along with a Twitter dataset we generated ourselves. For the latter, we used a Markov Chains model, trained on stories, geo-political and religious texts to create a sample dataset for us to use afterwards.

As to *how* we went about achieving our goals, we used techniques like *Language Recognition (LR)*, *Named Entiry Recognition (NER)* and *Sentiment Analysis (SA)*. All of these where applied to Tweets for us to be able to find out which ones would be worth considering for the analysis - basically filtering out all the Tweets that are not referencing a certain specific event. We then define *sentiment strength* with values from -1 to 1 (from the most negative to the most positive). To apply this measurement, we also filter out Tweets outside a time window centered on the conflict start's date, which then more accurately allows us to define the *impactfullness* of the event - this time in the range from 0 to 1 (from the least impactfull to the most impactfull).

We try and clarify our point through our main notebook. There, we showcase our whole pipeline and our methodology, while discussing the pros and cons of our approach to the problem - through statistics and plotting.

## Research questions

How to measure emotional value over a time-frame?

How to quantify emotional contrast, in Twiter, comparing *before* and *after* an event ocurs?

## Datasets

We opted to use two datasets:

1. UCDP
This dataset covers individual events of organized violence. We consider a subset of the conflicts in this dataset, and keep the relevant information for each of the conflicts.

2. Twitter
Because of time-constraints, in order to parse the dataset and retrieve the desired content, we decided that the approach wouldn't be possible for us. Therefore, we decided to implement our custom Tweet generator, using a Markov Chains based model.

### UCDP

  * From this dataset we plan on extracting conflicts based on their category - defined from *casualties*, *duration* and *involved parties*.
  * Because of that, we only need to keep information regarding the conflict's *name*, *location*, *start date*, *end date* and *type*. We will consider the country of the conflict as the *location*.

### Twitter

  * Before deciding to pivot on our final goal, we did attempt to fetch our data from the cluster (although to no avail). All the scripts used in these attempts are well documented and available within the Spark directory of the Project, complete with a full descriptive [README](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/README.md) file of the overall process (the last section of the README represents all our considerations and possible improvements). 
  * The *Language Recognition (LR)* module is used to retrieve only samples that are in English. It's important to note we made the assumption that the content of English Tweets alone is a good representation of the world's overall opinion.
  * For each time-frame, we do **Named Entity Recognition** (NER) to figure out the country it is talking about - discard all that don't mention countries of the conflicts we want.
  * For the remaining Tweets, we apply **Sentiment Analysis** on the text and store that information alongside the Tweets.
  * We then define the **Sentimental Impact** as a measure that reflects the contrast between the average daily *sentiment strength* before and after the conflict.

## Named Entity Recognition
For **Named Entity Recognition** we make use of a **Natural Language Processing** library called [Spacy](https://spacy.io/). With it, we use each country's *code*, *name*, *cities*, *common denomination*, *nationality*, *currency* and an estimate of its *religious affiliation* ratios for identifying the country that is being talked about in a Tweet (if there is one). For everything except the *religious affiliations*, we will use [mledoze's dataset](https://mledoze.github.io/countries/) and [maxmind's dataset](https://www.maxmind.com/de/free-world-cities-database). For the last component, we will simply consider the most common affiliations and from [globalreligiousfutures dataset](http://globalreligiousfutures.org/explorer#/?subtopic=15&chartType=map&year=2010&data_type=number&religious_affiliation=55&destination=to&countries=Worldwide&age_group=all&gender=all&pdfMode=false).

## Sentiment Analysis
For **Sentiment Analysis** we use [NLTK's Vader sentiment analyzer](http://www.nltk.org/_modules/nltk/sentiment/vader.html) - getting a *compund* value from -1.0 to 1.0. We keep this compound value so that we reduce the margin of error when doing daily averaging and calculating *sentimental impact* - whichi we ultimately categorize into *impactful* and *not impactful*.

## Project Structure

Although the main part of the project can be seen in the [project notebook](https://github.com/nunomota/ada2017-hw/blob/master/project/project.ipynb), there are other important directories than contain interesting information:

* [parsers](https://github.com/nunomota/ada2017-hw/tree/master/project/parsers): Contains notebooks specifically designed to parse and format the data from the used datasets
* [analyzers](https://github.com/nunomota/ada2017-hw/tree/master/project/analyzers): Contains notebooks that perform exploratory analysis on parsed datasets (to either help with feature selection or categorization)
* [filters](https://github.com/nunomota/ada2017-hw/tree/master/project/filters): Contains notebooks designed to filters the data parsed in a previous step
* [scripts](https://github.com/nunomota/ada2017-hw/tree/master/project/parsers): Contains python scripts to be used as modules for several steps of the project
* [data](https://github.com/nunomota/ada2017-hw/tree/master/project/data): Contains both the *raw* and *parsed* datasets generated by our notebooks - for memory concerns, the *raw* directory is zipped
* [spark](https://github.com/nunomota/ada2017-hw/tree/master/project/spark) : Contains python scripts used to attempt to retrieve the data from the Spark Cluster
* [report](https://github.com/nunomota/ada2017-hw/tree/master/project/report): Contains the report for the project

## Work Distribution

Nuno Goncalves: Data collection, data parsing, Twitter generator, NER
Lucia Montero: Data anlysis, data filtering, plotting
Matteo Yann Feo: Spark, SA, LR

Regardless of contribution areas, it's fair to say everyone contributed to every stepof the project.

## Presentation planning

Nuno Goncalves: Presentation preparation
Lucia Montero: Poster
Matteo Yann Feo: Poster