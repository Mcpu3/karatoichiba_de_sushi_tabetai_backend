from datetime import datetime, timedelta
import os
import dotenv
import tweepy
import random

from pn_predictor.predict_pns import predict_pns

dotenv.load_dotenv()
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

def set_client(at, ats) -> None:
    return tweepy.Client(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
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
        max_results = 13
    )

    l = []
    for t in str(tweets[0]).split(", "):
        t = t.translate(str.maketrans({"[": None, "]": None, "<": None, ">": None, "'": None}))
        t = t.replace("Tweet id=", "").replace("text=", "").replace("　", "").replace("\\n", "")
        if t != "None":
            l.append(t.split(" ", 1)[1])
    print(l)

    s = ""
    if l != []:
        f= predict_pns(l, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
        print(f)

        if f.count(1) >= f.count(-1) :
            number = random.randrange(3)
            if number == 0:
              s = "今日は一日楽しそうだったね！！いぇいいぇい"
            elif number == 1:
              s = "今日は一日を満喫だね！"
            elif number == 2:
                s = "今日は一日を満喫だね！"

        else :
            number = random.randrange(3)
            if number == 0 :
             s = "今日はネガティブガーン・・・・"
            elif number == 1:
              s = "今日はなんだか元気がないね・・"
            elif number == 2:
                s = "今日はなんだか悲しいそうだね・・・"
    else:
        number = random.randrange(3)
        if number == 0 :
             s = "今日は忙しかったのかな…… しっかり休んでね泣"
        elif number == 1:
              s = "なにもつぶやいてないってことは，現実が充実してる証拠だよ！"
        elif number == 2:
                s = "何もつぶやかないの？ウサ子さみしいな・・"
       

    client.create_tweet(text = s)

