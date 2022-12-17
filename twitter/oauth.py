from requests_oauthlib import OAuth1Session

import secret

consumer_key = secret.consumer_key
consumer_secret = secret.consumer_secret

callback_url = "https://twitter.com/megaro_sushi"
request_endpoint_url = "https://api.twitter.com/oauth/request_token"
authenticate_url = "https://api.twitter.com/oauth/authenticate"

session_req = OAuth1Session(consumer_key, consumer_secret)
response_req = session_req.post(request_endpoint_url, params={"oauth_callback": callback_url})
response_req_text = response_req.text

oauth_token_kvstr = response_req_text.split("&")
token_dict = {x.split("=")[0]: x.split("=")[1] for x in oauth_token_kvstr}
oauth_token = token_dict["oauth_token"]

print("Authentication URL:", f"{authenticate_url}?oauth_token={oauth_token}")
