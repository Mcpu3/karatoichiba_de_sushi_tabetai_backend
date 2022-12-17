from argparse import ArgumentParser
import csv
from pickle import load
from typing import Dict, List

import MeCab
import neologdn
from scipy.sparse import hstack


def predict_pns_by_dictionary(texts: List[str], dictionary_path: str='./pn.csv.m3.120408.trim', count_vectorizer_path: str='./count_vectorizer.pickle', model_path: str='./model.pickle') -> List[float]:
    __create_mecab__()
    dictionary = __get_dictionary__(dictionary_path)
    with open(count_vectorizer_path, 'rb') as f:
        count_vectorizer = load(f)
    for text in texts:
        text = neologdn.normalize(text)
    bag_of_words = count_vectorizer.transform(texts)
    pns = __get_pns__(texts, dictionary)
    x = hstack([bag_of_words, pns])
    with open(model_path, 'rb') as f:
        model = load(f)
    predicted_pns = model.predict(x)
    predicted_pns = predicted_pns.tolist()

    return predicted_pns

def __get_dictionary__(dictionary_path: str) -> Dict[str, int]:
    dictionary = {}
    with open(dictionary_path, encoding='utf-8') as f:
        raw = csv.reader(f, delimiter='\t')
        for row in raw:
            text = neologdn.normalize(row[0])
            if row[1] == 'e':
                pn = 0
            elif row[1] == 'p':
                pn = 1
            elif row[1] == 'n':
                pn = -1
            else:
                continue
            dictionary[text] = pn

    return dictionary

def __get_pns__(texts: List[str], dictionary: Dict[str, int]) -> List[int]:
    pns = []
    for text in texts:
        pn = [0]
        tokens = __get_tokens__(text)
        for token in tokens:
            if token not in dictionary:
                continue
            pn[0] += dictionary[token]
        pns.append(pn)

    return pns

def __get_tokens__(text: str) -> List[str]:
    tokens = []
    node = mecab.parseToNode(text)
    while node:
        if node.surface:
            tokens.append(node.surface)
        node = node.next

    return tokens

def __create_mecab__() -> None:
    global mecab
    mecab = MeCab.Tagger()

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--dictionary_path', default='./pn.csv.m3.120408.trim')
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    __create_argument_parser__()
    texts_size = int(input('Texts size: '))
    texts = [input(f'Texts[{i}]: ') for i in range(texts_size)]
    predicted_pns = predict_pns_by_dictionary(texts, args.dictionary_path, args.count_vectorizer_path, args.model_path)
    for text, predicted_pn in zip(texts, predicted_pns):
        print(text + ': ' + str(predicted_pn))

if __name__ == '__main__':
    __main__()