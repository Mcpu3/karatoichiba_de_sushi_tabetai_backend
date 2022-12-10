## tweepyの導入<br/>
`pip install tweepy`<br/>

## Botの動かし方<br/>
* **GitHubに公開されない新しいファイルを作成**<br/>
(`bot_secret.py`という名前のファイルはGitにコミットされないようになっているため分からなければこの名前にしておけばOK)<br/>
* 作ったファイルにbot.pyのコードを全てコピー<br/>
* `tweepy.client()`の中にDiscordで共有した各種トークンをコピペ<br/>
* ターミナルで実行<br/>

## コミットの前に
`bot.py`の中にトークンが書かれていないか必ず確認してからコミットすること<br/>
基本的には上で作った`bot_secret.py`の中で作業するとGood