# World conflicts' information proliferation

## Abstract

The aim of the project is to quantify the *sentimental impact* a certain world event, as conflicts around the globe, had on the Twitter community. 

In order to reach this goal, we have used the UCDP dataset, as our focus is centered around conflicts, along with a Twitter samples dataset we delivered. For the latter, we have have trained a model, based on Markov Chains, on stories, geo-political and religious texts to generate Twitter samples and populate the dataset.

As to *how* we will deliver the task, we have used techniques like *Language Recognition (LR)*, *Named Entiry Recognition (NER)* and *Sentiment Analysis (SA)* to find out which Tweets are worth considering for the analysis in relation to a certain conflic of interest. We can therefore define the *sentiment strength* characteristic (not if they are *positive*, *negative* or *neutral* but their *strength* from 0.0 to 1.0) of such tweet's samples. Analysing the *sentiment strength* around a time window (before and after) centered on the conflict start's date, we have been able to define the *impactfullness* of the event in the same range of values (from 0.0 to 1.0).

We will make that information clear by showcasing scenarios in which we pipeline our methodology while discussing the pros and cons of our approach to the problem - through statistics and plotting - while tackling each step into the analysis.

## Research questions

How to quantify emotional contrast, in Twiter, comparing *before* and *after* a conflict arises?

If so, is this more noticeable for certain categories of conflicts? Or does this vary by location?

## Datasets

We opted to use two datasets:

1. UCDP
This dataset covers individual events of organized violence. We consider a subset of the conflicts in this dataset, and keep the relevant information for each of the conflicts.

2. Twitter
Through an in-depth analysis in order to parse the dataset and retrieve the desired content, we decided that the approach couldn't reach efficient results from a time-wise prospective. We therefore decided to implement our custom dataset generatet by the training of a Markov Chains based model.

### UCDP

  * From this dataset we plan on extracting conflicts based on their category - defined from *casualties*, *duration* and *involved parties*.
  * Because of that, we only need to keep information regarding the conflict's *name*, *location*, *start date*, *end date* and *type*. We will consider the country of the conflict as the *location*.

### Twitter

  * We delivered a complete parsing job on the Twitter dataset provided, only to realize that results could't get delivered efficiently (time-wise). We have nevertheless implemented an entire collection of Scripts to process the data via Spark that can be see in the Spark directory of the Project, complete with a full descriptive [README](https://github.com/nunomota/ada2017-hw/blob/master/project/spark/README.md) file of the overall process. 
  * In order to obtain a population of Twitter samples we have opted for a model that, based on Markov Chains, generated samples on themes it was trained on. We provided those latters as a collection of stories, geo-political and religious texts to obtain content in line with the needs.
  * The *Language Recognition (LR)* module is used to retrieve only samples that are in English. It's important to note we made the assumption that the content of English Tweets alone is a good representation of the world's overall opinion.
  * For each time-frame, we do **Named Entity Recognition** (NER) to figure out the country it is talking about - discard all that don't mention countries of conflict.
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

## Completed Milestones

1. Perform **Named Entity Recognition** on Tweets
2. Perform **Sentiment Analysis** on Tweets
3. Initial filtering on UCDP dataset
4. Perform **Language Recognition** on Tweets