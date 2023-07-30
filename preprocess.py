import re
import string
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_tweet(tweet):
    """
    Clean the tweet by removing URLs, mentions, and special characters.
    """
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'@\w+ ?', '', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    return tweet.strip()

def remove_stopwords(tweet):
    """
    Remove stop words from the tweet.
    """
    return ' '.join([word for word in tweet.split() if word.lower() not in stop_words])

def get_subjectivity(tweet):
    """
    Get the subjectivity of the tweet.
    """
    return TextBlob(tweet).sentiment.subjectivity

def get_polarity(tweet):
    """
    Get the polarity of the tweet.
    """
    return TextBlob(tweet).sentiment.polarity
