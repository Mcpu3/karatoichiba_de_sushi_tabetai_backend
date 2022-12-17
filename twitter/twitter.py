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

start_time = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
print(start_time)

query = "-is:retweet to:" + secret.id

while 1:
    
    end_time = datetime.now().replace(second=0, microsecond=0)
    tweets = client.search_recent_tweets(
        query = query,
        start_time = str(start_time.isoformat()) + "+09:00",
        end_time = str(end_time.isoformat()) + "+09:00"
    )

    if tweets is not None:
        print(tweets[0])

    start_time = datetime.now().replace(second=0, microsecond=0)
    time.sleep(60)