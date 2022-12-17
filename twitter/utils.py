import json

# JSONを読み込んでdataとして返す関数
def json_load():
    json_read = open("token.json", "r")
    data = json.load(json_read)
    json_read.close()
    return data

# dataを引数としてJSONに書き込む関数
def json_write(data):
    json_write = open("token.json", "w")
    json.dump(data, json_write, indent=4, ensure_ascii=False)
    json_write.close()