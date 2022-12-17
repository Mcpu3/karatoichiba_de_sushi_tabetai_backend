from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session
from . import secret

consumer_key = secret.consumer_key
consumer_secret = secret.consumer_secret

base_url = "https://api.twitter.com/"
request_token_url = base_url + "oauth/request_token"
authenticate_url = base_url + "oauth/authenticate"
access_token_url = base_url + "oauth/access_token"

def get_twitter_request_token(oauth_callback):

    twitter = OAuth1Session(consumer_key, consumer_secret)
    response = twitter.post(
        request_token_url,
        params={"oauth_callback": oauth_callback}
    )

    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから認証画面のURLを生成
    authenticate_endpoint = "%s?oauth_token=%s" \
        % (authenticate_url, request_token["oauth_token"])

    request_token.update({"authenticate_endpoint": authenticate_endpoint})
    return request_token["authenticate_endpoint"]


def get_twitter_access_token(oauth_token, oauth_verifier):

    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
    )

    response = twitter.post(
        access_token_url,
        params={"oauth_verifier": oauth_verifier}
    )

    access_token = dict(parse_qsl(response.content.decode("utf-8")))
    return access_token