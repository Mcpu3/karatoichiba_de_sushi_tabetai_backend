from datetime import datetime,timedelta
import time
import tweepy

import secret

client = tweepy.Client(
    consumer_key = secret.consumer_key,
    consumer_secret = secret.consumer_secret,
    access_token = secret.access_token,
    access_token_secret = secret.access_token_secret,
    bearer_token = secret.bearer_token
)

query = "-is:retweet to:" + secret.id

tweets = client.search_recent_tweets(query = query, max_results = 10)

if tweets is not None:
    for tweet in tweets:
        print(tweet)