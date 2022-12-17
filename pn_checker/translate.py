import requests

API_KEY = '5ec95d97-cd5c-222b-8684-17eefdf88e7c:fx' # 自身の API キーを指定

def translate(source_lang: str, target_lang: str, source_text: str) -> str:
    # パラメータの指定
    params = {
                'auth_key' : API_KEY,
                'text' : source_text,
                'source_lang' : source_lang, # 翻訳対象の言語
                "target_lang": target_lang  # 翻訳後の言語
            }

    # リクエストを投げる
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params) # URIは有償版, 無償版で異なるため要注意
    result = request.json()
    output_text = result['translations'][0]['text']
    return output_text

def translate_list(source_lang: str, target_lang: str, source_text_list: list) -> list:
    output_text_list = []
    for source_text in source_text_list:
        result = translate(source_lang, target_lang, source_text)
        output_text_list.append(result)

    return output_text_list