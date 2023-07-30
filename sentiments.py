from textblob import TextBlob
import pandas as pd


def get_sentiment(tweet):
    """
    Get the sentiment of the tweet (positive, negative, or neutral).
    """
    sentiment = TextBlob(tweet).sentiment.polarity
    if sentiment > 0:
        return 'Positive'
    elif sentiment < 0:
        return 'Negative'
    else:
        return 'Neutral'


def add_sentiment(df):
    """
    Add sentiment to each tweet in the DataFrame.
    """
    df['Sentiment'] = df['Tweet'].apply(get_sentiment)
    return df
