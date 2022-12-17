import tweepy

import secret

client = tweepy.Client(
    consumer_key=secret.consumer_key,
    consumer_secret=secret.consumer_secret,
    access_token=secret.access_token,
    access_token_secret=secret.access_token_secret
)

text = input("Tweet?>")
client.create_tweet(text = text)
