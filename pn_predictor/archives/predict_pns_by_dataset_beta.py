from argparse import ArgumentParser
from pickle import load
from typing import List

import pyinflect
import spacy


def predict_pns_by_dataset(texts: List[str], count_vectorizer_path: str='./count_vectorizer.pickle', model_path: str='./model.pickle') -> List[int]:
    with open(count_vectorizer_path, 'rb') as f:
        count_vectorizer = load(f)
    bag_of_words = count_vectorizer.transform(texts)
    x = bag_of_words
    with open(model_path, 'rb') as f:
        model = load(f)
    predicted_pns = model.predict(x)
    predicted_pns = predicted_pns.tolist()

    return predicted_pns

def __get_tokens__(text: str) -> List[str]:
    tokens = []
    raw = nlp(text)
    for row in raw:
        token = row.text
        if row.pos_ == 'NOUN':
            inflected = row._.inflect('NN', inflect_oov=True)
            if inflected is not None:
                token = inflected
        elif row.pos_ == 'VERB':
            inflected = row._.inflect('VB', inflect_oov=True)
            if inflected is not None:
                token = inflected
        elif row.pos_ == 'ADJ':
            inflected = row._.inflect('JJ', inflect_oov=True)
            if inflected is not None:
                token = inflected
        elif row.pos_ == 'ADV':
            inflected = row._.inflect('RB', inflect_oov=True)
            if inflected is not None:
                token = inflected
        tokens.append(token)

    return tokens

def __create_spacy__() -> None:
    global nlp
    nlp = spacy.load('en_core_web_sm')

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    __create_argument_parser__()
    texts_size = int(input('Texts size: '))
    texts = [input(f'Texts[{i}]: ') for i in range(texts_size)]
    predicted_pns = predict_pns_by_dataset(texts, args.count_vectorizer_path, args.model_path)
    for text, predicted_pn in zip(texts, predicted_pns):
        print(text + ': ' + str(predicted_pn))

if __name__ == '__main__':
    __main__()