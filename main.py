import time
from datetime import datetime, timedelta
from flask import Flask, render_template, session
from flask import url_for, redirect, request

from pn_predictor.predict_pns import predict
import twitter.secret as secret
import twitter.reply as reply
import twitter.oauth as oauth

app = Flask(__name__)
app.secret_key = "howgohwpei3gjapo.dp@dapoihgw:98k"

@app.route("/")
def index():
    if "user_name" in session:
        user_name = session["user_name"]
    else:
        user_name = []
    return render_template("index.html", user_name=user_name)

@app.route("/oauth_register")
def redirect_oauth():
    oauth_callback = request.args.get("oauth_callback")
    callback = oauth.get_twitter_request_token(oauth_callback)
    return redirect(callback)

@app.route("/callback")
def execute_userinfo():

    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    access_token = oauth.get_twitter_access_token(
        oauth_token, oauth_verifier)

    session["user_name"] = access_token["screen_name"]
    session["user_id"] = access_token["user_id"]
    session["oauth_token"] = access_token["oauth_token"]
    session["oauth_token_secret"] = access_token["oauth_token_secret"]
    
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    session.pop("user_id", None)
    session.pop("oauth_token", None)
    session.pop("oauth_secret", None)
    return redirect(url_for("index"))

def __main__() -> None:

    rp_client = reply.set_client(secret.consumer_key, secret.consumer_secret, secret.access_token, secret.access_token_secret, secret.bearer_token)
    start_time = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
    query = "-is:retweet to:" + secret.id
    print(start_time)

    app.run(debug=True)

    while 1:
        start_time = reply.stream(rp_client, query, start_time, secret.id)
        print(start_time)
        time.sleep(60)

if __name__ == "__main__":
    __main__()