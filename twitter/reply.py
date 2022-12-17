from datetime import datetime, timedelta

from pn_predictor.predict_pns import predict

def stream(client, query, start_time, id) -> None:

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
            t = t.replace("Tweet id=", "").replace("text=", "").replace("@"+id, "").replace("\n", "")
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
                    t = t.replace("Tweet id=", "").replace("text=", "").replace("　", "").replace("\n", "")
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

    return datetime.now().replace(second=0, microsecond=0)

