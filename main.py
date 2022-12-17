from datetime import datetime, timedelta
import time
import tweepy

from pn_predictor.predict_pns import predict
import twitter.secret as secret

client = tweepy.Client(
    consumer_key = secret.consumer_key,
    consumer_secret = secret.consumer_secret,
    access_token = secret.access_token,
    access_token_secret = secret.access_token_secret,
    bearer_token = secret.bearer_token
)

def __main__() -> None:

    start_time = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
    query = "-is:retweet to:" + secret.id
    print(start_time)

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
                t = t.replace("Tweet id=", "").replace("text=", "").replace("@"+secret.id, "").replace("\n", "")
                if t != "None":
                    data.append([t.split(" ", 1)[0], t.split(" ", 1)[1]])

            for p in data:

                s = str(p[1])
                now = datetime.now().replace(second=0, microsecond=0)
                before24h = (datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0)

                if s.count(" ") + s.count("　") == len(s):
                    s = "リプが空っぽだよ！"

                else:

                    tweets = client.search_recent_tweets(
                        query = s,
                        start_time = str(before24h.isoformat()) + "+09:00",
                        end_time = str(now.isoformat()) + "+09:00"
                    )

                    l = []
                    for t in str(tweets[0]).split(", "):
                        t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
                        t = t.replace("Tweet id=", "").replace("text=", "").replace("@"+secret.id, "").replace("　", "").replace("\n", "")
                        print(t)
                        if t != "None":
                            l.append(t.split(" ", 1)[1])
                    print(l)

                    if l != []:
                        f= predict(l, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
                        print(f)

                        if f.count(1) >= f.count(-1):
                            s += " のことはみんな大好きみたいだよ！"
                        else :
                            s += " のことはあんまり良く思われてないみたい……"
                    else:
                        s += " について話してる人はいなかったみたい……"

                client.create_tweet(text = s, in_reply_to_tweet_id = p[0])

        start_time = datetime.now().replace(second=0, microsecond=0)
        print(start_time)
        time.sleep(60)

if __name__ == '__main__':
    __main__()