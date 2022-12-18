import time
from datetime import datetime, timedelta

from flask import Flask
import twitter.auto as auto
import twitter.secret as secret
import twitter.reply as reply
import twitter.utils as utils


app = Flask(__name__)
app.secret_key = "howgohwpei3gjapo.dp@dapoihgw:98k"

@app.route('/')
def __main__() -> None:
    rp_client = reply.set_client()
    start_time = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
    query = "-is:retweet to:" + secret.id
    print(start_time)

    while 1:

        start_time = reply.stream(rp_client, query, start_time)

        auto_tweet_time = "0000"
        if datetime.now().strftime("%H%M") == auto_tweet_time: 
            data = utils.json_load()
            for tk in data:
                client = auto.set_client(data[tk][1], data[tk][2])
                auto.stream(client, rp_client, data[tk][0])

        print(start_time)
        time.sleep(60)

if __name__ == "__main__":
    __main__()