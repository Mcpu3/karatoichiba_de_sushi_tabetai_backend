from datetime import datetime, timedelta
import time

from pn_predictor.predict_pns import predict
import twitter.secret as secret
import twitter.reply as reply

def __main__() -> None:

    rp_client = reply.set_client(secret.consumer_key, secret.consumer_secret, secret.access_token, secret.access_token_secret, secret.bearer_token)
    start_time = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
    query = "-is:retweet to:" + secret.id
    print(start_time)

    while 1:
        start_time = reply.stream(rp_client, query, start_time, secret.id)
        print(start_time)
        time.sleep(60)

if __name__ == '__main__':
    __main__()