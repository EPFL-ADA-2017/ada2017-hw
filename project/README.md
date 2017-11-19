# Title

## Abstract

For our project we decided to make use of both UCDP and Twitter datasets. From these, we would like to figure out any existing gaps in the information proliferation around the globe, regarding the conflicts' locations.

As to *how* we will make that information clear, we decided to create a Machine Learning (ML) model to study Twitter's history - around certain conflicts' dates - and make predictions as to what would happen if a conflict *x* would arise in region *y*. This model takes into account the result of **Sentiment Analysis** over the selected time-frame and outputs the expected sentiments for a hypothetically new time-frame around the speculated conflict. Would people show the same emotions we are expecting them to? Or would they seem to ignore this fact and maintain their normal behavior?

We thought it would be interesting to shed some light on world-wide situations to which the general public might be oblivious to, hence our approach to the problem. Bear in mind, our purpose is not to figure out *why* these differences may exist (e.g. political or media influences) but *where* they exist.

## Research questions
Is there a noticeable difference between the *expected* and *actual* emotions towards certain kinds of conflicts (and/or regions)?

If so, which conflicts (or regions) are the ones most notoriously affected by it?

## Dataset
List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.

1. UCDP
 * From this dataset we plan on extracting conflicts based on their importance - measured from *casualties*, *duration* and *involved parties*.
 * After this, we only need to keep information regard the conflict's *name*, *start date*, *end date* and *type*.
2. Twitter
 * From this dataset we plan on keeping only the Tweets around a couple days time-frame around the kept conflicts.
 * After the initial filtering, we need only the Tweets' *content* and their *date* (discarding any other information).
 * For each time-frame, we do **Name Entity Recognition** (NER) to figure out the country it is talking about - keeping only the ones talking about the countries of conflict.
 * For the remaining Tweets, we apply **Sentiment Analysis** on the text and store that information alongside the Tweets.
 * We now use this information to train our model.

For both **Name Entity Recognition** and **Sentiment Analysis** we will make use of **Natural Language Processing** libraries, such as [Spacy](https://spacy.io/) and [NLTK](http://www.nltk.org/). Also, we will need each country's *code*, *name*, *common denomination*, *nationality*, *currency* and an estimate of its *religious affiliation* ratios. For everything except the *religious affiliations*, we will use [mledoze's dataset](https://mledoze.github.io/countries/). For the last component, we will simply consider the most common affiliations and use [globalreligiousfutures dataset](http://globalreligiousfutures.org/explorer#/?subtopic=15&chartType=map&year=2010&data_type=number&religious_affiliation=55&destination=to&countries=Worldwide&age_group=all&gender=all&pdfMode=false).

## Personal Milestones (until milestone 2)

1. Initial filtering on Twitter and UCDP datasets
2. Conflict categorization on certain criteria
3. Time-frame filtering on Twitter
4. Perform **Name Entity Recognition** on tweets
5. Perform **Sentiment Analysis** on tweets

## Questions for TAa

1. Does the Twitter dataset contain the Tweets' dates?
