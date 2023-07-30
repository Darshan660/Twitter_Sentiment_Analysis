# importing the required libraries
import tweepy
import pandas as pd
from preprocess import clean_tweet
from preprocess import remove_stopwords
from preprocess import get_subjectivity
from preprocess import get_polarity
from sentiments import add_sentiment
import os


# twitter credentials
# keys and tokens from the twitter developer account
consumer_key = 'sdXBrqd34mtf1x096ulUmz8ad'
consumer_secret = 'hvwK0LQjEY0zPyDNNKXAyj4RlYjpvqRLdk8yXqC6811o8GIAqE'
access_token = '1143565458622181376-6O9pbiljs30pDHmuX4goBsnnOksKQW'
access_token_secret = '4xChwxskSlaGisWinvZXVy31GDsgPTnzH0JHFhgy2nlkl'


# attempt authentication
try:
    # create OAuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth,wait_on_rate_limit=True)
except:
    print("Error: Authentication Failed")


def get_tweets(keyword, count=1000):
    """
    Get tweets containing the given keyword.
    """
    tweets = tweepy.Cursor(api.search_tweets,
                           q=keyword,
                           lang='en').items(count)

    return [{'Tweet': clean_tweet(tweet.text),
             'Timestamp': tweet.created_at,
             'Subjectivity': get_subjectivity(tweet.text),
             'Polarity': get_polarity(tweet.text)} for tweet in tweets]

def analyze_tweets(keyword, count=1000):
    """
    Analyze tweets containing the given keyword.
    """
    tweets = get_tweets(keyword, count)
    df = pd.DataFrame(tweets)
    df = add_sentiment(df)


    return df
