from flask import Flask, render_template, session
from flask import url_for, redirect, request

import twitter.oauth as oauth
import twitter.utils as utils

app = Flask(__name__)
app.secret_key = "howgohwpei3gjapo.dp@dapoihgw:98k"

@app.route("/")
def index() -> None:
    if "user_name" in session:
        user_name = session["user_name"]
    else:
        user_name = []
    return render_template("index.html", user_name=user_name)

@app.route("/oauth_register")
def redirect_oauth() -> None:
    oauth_callback = request.args.get("oauth_callback")
    callback = oauth.get_twitter_request_token(oauth_callback)
    return redirect(callback)

@app.route("/callback")
def execute_userinfo() -> None:

    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    access_token = oauth.get_twitter_access_token(
        oauth_token, oauth_verifier)

    session["user_name"] = access_token["screen_name"]
    session["user_id"] = access_token["user_id"]
    session["oauth_token"] = access_token["oauth_token"]
    session["oauth_token_secret"] = access_token["oauth_token_secret"]

    data = utils.json_load()
    data[session["user_name"]] = [access_token["oauth_token"], access_token["oauth_token_secret"]]
    utils.json_write(data)

    return redirect(url_for("index"))

@app.route("/logout")
def logout() -> None:

    data = utils.json_load()
    del data[session["user_name"]]
    utils.json_write(data)

    session.pop("user_name", None)
    session.pop("user_id", None)
    session.pop("oauth_token", None)
    session.pop("oauth_secret", None)

    return redirect(url_for("index"))

app.run(debug=True)
