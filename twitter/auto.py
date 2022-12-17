from datetime import datetime, timedelta
import tweepy

from pn_predictor.predict_pns import predict
from . import secret

def set_client(at, ats) -> None:
    return tweepy.Client(
        consumer_key = secret.consumer_key,
        consumer_secret = secret.consumer_secret,
        access_token = at,
        access_token_secret = ats
    )

def stream(client, rp_client, user_name) -> None:

    now = datetime.now().replace(second=0, microsecond=0)
    before1d = (datetime.now() - timedelta(days=1) + timedelta(minutes=3)).replace(second=0, microsecond=0)

    tweets = rp_client.search_recent_tweets(
        query = "-is:retweet from:" + user_name,
        start_time = str(before1d.isoformat()) + "+09:00",
        end_time = str(now.isoformat()) + "+09:00",
        max_results = 100
    )

    l = []
    for t in str(tweets[0]).split(", "):
        t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
        t = t.replace("Tweet id=", "").replace("text=", "").replace("　", "").replace("\n", "")
        if t != "None":
            l.append(t.split(" ", 1)[1])
    print(l)

    s = ""
    if l != []:
        f= predict(l, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
        print(f)

        if f.count(1) >= f.count(-1):
            s = "今日は楽しそうだったね！ Botより"
        else :
            s = "今日はあんまり調子がでなかったのかな…… Botより"
    else:
        s = "今日は忙しかったのかな…… Botより"

    client.create_tweet(text = s)

