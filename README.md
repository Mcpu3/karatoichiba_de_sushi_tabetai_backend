# ライブラリの導入
`pip install -r requirements.txt`<br/>

# Botの動かし方
* ルートディレクトリに`.env`ファイルを作成しDiscordで共有した内容をコピペ<br/>
* ターミナルで`py main.py`と`py server.py`を実行<br/>

# PN予測

## `pn_predictor/`
1. <https://www.kaggle.com/datasets/kazanova/sentiment140/download?datasetVersionNumber=2>からデータセットをダウンロードし、`training.1600000.processed.noemoticon.csv`を`pn_predictor/misc/`下にコピーする。
1. 以下を実行する。
```sh
unzip pn_predictor/misc/count_vectorizer.zip -d pn_predictor/misc/
unzip pn_predictor/misc/model.zip -d pn_predictor/misc/
```

=======