from argparse import ArgumentParser
from typing import List

from .misc.predict import predict
from .misc.translate import translate_list


def predict_pns(texts: List[str], count_vectorizer_path: str, model_path: str) -> List[int]:
    translated_texts = translate_list('JA', 'EN', texts)
    print(translated_texts)
    predicted_pns = predict(translated_texts, count_vectorizer_path, model_path)

    return predicted_pns

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    texts_size = int(input('Texts size: '))
    texts = [input(f'Texts[{i}]: ') for i in range(texts_size)]
    predicted_pns = predict_pns(texts, args.count_vectorizer_path, args.model_path)
    for text, predicted_pn in zip(texts, predicted_pns):
        print(text + ': ' + str(predicted_pn))

if __name__ == '__main__':
    __main__()