'''
Title: Language Recognition with langdetect

The purpose of this notebook is to perform language analysison a Tweet. This allows an automatic filtering on the Tweets by language (making sure we only perform **Name Entity Recognition** and **Sentiment Analysis** on English texts).
'''

import langdetect

def is_tweet_english(tweet_text):
    '''
    This method returns whether or not
    a Tweet's text is in English.
    '''
    return langdetect.detect(tweet_text) == 'en'