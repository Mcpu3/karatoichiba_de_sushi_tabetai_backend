from datetime import datetime, timedelta
import os
import dotenv
import tweepy

from pn_predictor.predict_pns import predict_pns

dotenv.load_dotenv()
id = os.environ["ID"]
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
bearer_token = os.environ["BEARER_TOKEN"]

def set_client() -> None:
    return tweepy.Client(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret,
        bearer_token = bearer_token
    )

def stream(client, query, start_time) -> None:

    end_time = datetime.now().replace(second=0, microsecond=0)
    tweets = client.search_recent_tweets(
        query = query,
        start_time = str(start_time.isoformat()) + "+09:00",
        end_time = str(end_time.isoformat()) + "+09:00",
        max_results = 20
    )

    data = []
    if tweets is not None:
        for t in str(tweets[0]).split(", "):
            t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
            t = t.replace("Tweet id=", "").replace("text=", "").replace("@" + id, "").replace("\n", "")
            if t != "None":
                data.append([t.split(" ", 1)[0], t.split(" ", 1)[1]])

        for p in data:

            s = str(p[1])
            now = datetime.now().replace(second=0, microsecond=0)
            before3d = (datetime.now() - timedelta(days=3)).replace(second=0, microsecond=0)

            if s.count(" ") + s.count("　") == len(s):
                s = "リプが空っぽだよ！"

            else:

                tweets = client.search_recent_tweets(
                    query = "-is:retweet " + s,
                    start_time = str(before3d.isoformat()) + "+09:00",
                    end_time = str(now.isoformat()) + "+09:00",
                    max_results = 20
                )

                l = []
                for t in str(tweets[0]).split(", "):
                    t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
                    t = t.replace("Tweet id=", "").replace("text=", "").replace("　", "").replace("\n", "")
                    if t != "None":
                        l.append(t.split(" ", 1)[1])
                print(l)

                if l != []:
                    f= predict_pns(l, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
                    print(f)

                    if f.count(1) >= f.count(-1):
                        s += "のことはみんな大好きみたいだよ！"
                    else :
                        s += "のことはあんまり良く思われてないみたい……"
                else:
                    s += "について話してる人はいなかったみたい……"

            client.create_tweet(text = s, in_reply_to_tweet_id = p[0])

    return datetime.now().replace(second=0, microsecond=0)

