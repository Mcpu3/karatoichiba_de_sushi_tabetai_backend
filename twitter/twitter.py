from datetime import datetime, timedelta
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
query = "-is:retweet to:" + secret.id

while 1:
    
    end_time = datetime.now().replace(second=0, microsecond=0)
    tweets = client.search_recent_tweets(
        query = query,
        start_time = str(start_time.isoformat()) + "+09:00",
        end_time = str(end_time.isoformat()) + "+09:00"
    )

    data = []
    if tweets is not None:
        for t in str(tweets[0]).split(", "):
            t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
            t = t.replace("Tweet id=", "").replace("text=", "").replace("@megaro_sushi", "").replace("\n", "")
            print(t)
            if t != "None":
                data.append([t.split(" ", 1)[0], t.split(" ", 1)[1]])

        for p in data:
            text = p[1]
            client.create_tweet(text = text, in_reply_to_tweet_id = p[0])
            print(text)

    start_time = datetime.now().replace(second=0, microsecond=0)
    print("Done")
    time.sleep(60)