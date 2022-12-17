import tweepy

client = tweepy.Client(
    consumer_key='',
    consumer_secret='',
    access_token='',
    access_token_secret=''
)

client.create_tweet(text = "Hello World")
