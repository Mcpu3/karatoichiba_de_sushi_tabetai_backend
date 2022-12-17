## tweepyの導入<br/>
`pip install tweepy`<br/>

## Botの動かし方<br/>
* **GitHubに公開されない新しいファイルを作成**<br/>
(`twitter_secret.py`という名前のファイルはGitにコミットされないようになっているため分からなければこの名前にしておけばOK)<br/>
* 作ったファイルに`twitter.py`のコードを全てコピー<br/>
* `tweepy.client()`の中にDiscordで共有した各種トークンをコピペ<br/>
* ターミナルで実行<br/>

## コミットの前に
`twitter.py`の中にトークンが書かれていないか必ず確認してからコミットすること<br/>
基本的には上で作った`twitter_secret.py`の中で作業するとGood