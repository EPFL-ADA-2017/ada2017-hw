'''
Title: Setiment Analysis with NLTK

The purpose of this notebook is to perform **Sentiment Analysis** on Tweets. Instead of returning *negative*, *neutral* or *positive* we decided to return the *compound* value to reduce the margin of error while daily-averaging these results down the line.
'''

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment_intensity(tweet_text):
    '''
    This method returns the sentiment intensity
    within a certain Tweet's text (from -1.0 to 1.0).
    '''
    sentiment_analyser = SentimentIntensityAnalyzer()
    polarity_scores = sentiment_analyser.polarity_scores(tweet_text)
    return polarity_scores['compound']