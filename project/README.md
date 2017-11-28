# World conflicts' information proliferation

## Abstract

For our project we decided to make use of both UCDP and Twitter datasets. From these, we would like to figure out any existing gaps in the information proliferation around the globe, regarding the conflicts' locations.

As to *how* we will make that information clear, we decided to create a predictive model. This model takes a conflicts' *category* and *country* as features and tries to predict the *sentimental impact* on Twitter. To do this, we will use techniques like *Named Entity Recognition* and *Sentiment Analysis* to find out which Tweets are worth considering, for a given conflict, and their *sentiment strength* (not if they are *positive*, *negative* or *neutral* but their *strength* from 0.0 to 1.0). Analysing the *sentiment strength* before and after a conflict's start date, we would then define *sentimental impact* in the same range of values (from 0.0 to 1.0). Applying a threshold to the results would give us either *impactful* or *not impactful* - which is what our model will try to predict. Would people show stronger emotions towards a country where a conflict arose? Or would they seem to ignore this fact and maintain their normal behavior?

We thought it would be interesting to shed some light on world-wide situations to which the general public might be oblivious to, hence our approach to the problem. Bear in mind, our purpose is not to figure out *why* these differences may exist (e.g. political or media influences) but *where* they exist.

## Research questions

Is there a noticeable difference between the *expected* and *actual* emotions towards certain kinds of conflicts (and/or regions)?

If so, which conflicts (or regions) are the ones most notoriously affected by it?

## Datasets

We opted to use two datasets:

1. UCDP
This dataset covers individual events of organized violence. We consider a subset of the conflicts in this dataset, and keep the relevant information for each of the conflicts.

2. Twitter
Through *Language Recognition*, we will only take into account the Tweets in English - so the emotions considered for our analysis are those of English-speaking Twitter users. We will also filter the dataset according to the date, keeping only the Tweets around certain time-frames.

### UCDP

  * From this dataset we plan on extracting conflicts based on their category - defined from *casualties*, *duration* and *involved parties*.
  * Because of that, we only need to keep information regarding the conflict's *name*, *location*, *start date*, *end date* and *type*. We will consider the country of the conflict as the *location*.

### Twitter

  * We plan on keeping only the Tweets in English published a couple days away (before and after) from the kept conflicts' start dates.
  * After the initial filtering, we need only the Tweets' *content* and their *date* (discarding any other information).
  * For each time-frame, we do **Named Entity Recognition** (NER) to figure out the country it is talking about - discard all that don't mention countries of conflict.
  * For the remaining Tweets, we apply **Sentiment Analysis** on the text and store that information alongside the Tweets.
  * We then define the **Sentimental Impact** as a measure that reflects the contrast between the average daily *sentiment strength* before and after the conflict.
  * We now use this information to train our model, that we will use to predict the **Sentiment Impact** for certain conflicts (either real or hypothetical).

#### Named Entity Recognition
For both **Named Entity Recognition** and **Sentiment Analysis** we will make use of **Natural Language Processing** libraries, such as [Spacy](https://spacy.io/) and [NLTK](http://www.nltk.org/).

For **Named Entity Recognition** we use each country's *code*, *name*, *cities*, *common denomination*, *nationality*, *currency* and an estimate of its *religious affiliation* ratios for identifying the country that is being talked about in a Tweet (if there is one). For everything except the *religious affiliations*, we will use [mledoze's dataset](https://mledoze.github.io/countries/). For the last component, we will simply consider the most common affiliations and use [globalreligiousfutures dataset](http://globalreligiousfutures.org/explorer#/?subtopic=15&chartType=map&year=2010&data_type=number&religious_affiliation=55&destination=to&countries=Worldwide&age_group=all&gender=all&pdfMode=false).

For **Sentiment Analysis** we use [NLTK's NaiveBayes classifier](http://www.nltk.org/_modules/nltk/classify/naivebayes.html) - getting positive, negative and neutral Tweets.

## Completed Milestones

1. Perform **Named Entity Recognition** on Tweets
2. Perform **Sentiment Analysis** on Tweets
3. Initial filtering on UCDP dataset
4. Perform **Language Recognition** on Tweets