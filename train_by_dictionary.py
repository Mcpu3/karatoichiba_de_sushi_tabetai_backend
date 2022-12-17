from argparse import ArgumentParser
import csv
import json
import os
from pickle import dump
import re
from typing import Dict, List

import MeCab
import neologdn
from scipy.sparse import hstack
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


def train_by_dictionary(dictionary_path: str='./pn.csv.m3.120408.trim', dataset_directory: str='./chABSA-dataset/', count_vectorizer_path: str='./count_vectorizer.pickle', model_path: str='./model.pickle') -> None:
    __create_mecab__()
    dictionary = __get_dictionary__(dictionary_path)
    dataset = __get_dataset__(dictionary, dataset_directory, count_vectorizer_path)
    model = __get_model__()
    model.fit(dataset['x'], dataset['y'])
    with open(model_path, 'wb') as f:
        dump(model, f)

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

def __get_dataset__(dictionary: Dict[str, int], dataset_directory: str, count_vectorizer_path: str) -> Dict:
    x, y = [], []
    texts = []
    for path in os.listdir(dataset_directory):
        if re.fullmatch(r'e\d{5}_ann.json', path) is None:
            continue
        with open(os.path.join(dataset_directory, path), encoding='utf-8') as f:
            raw = json.load(f)
        for sentence in raw['sentences']:
            pn = 0
            for opinion in sentence['opinions']:
                if opinion['polarity'] == 'positive':
                    pn += 1
                elif opinion['polarity'] == 'negative':
                    pn -= 1
            y.append(pn)
            text = neologdn.normalize(sentence['sentence'])
            texts.append(text)
    count_vectorizer = CountVectorizer(tokenizer=__get_tokens__)
    bag_of_words = count_vectorizer.fit_transform(texts)
    with open(count_vectorizer_path, 'wb') as f:
        dump(count_vectorizer, f)
    pns = __get_pns__(texts, dictionary)
    x = hstack([bag_of_words, pns])
    dataset = {'x': x, 'y': y}

    return dataset

def __get_pns__(texts: List[str], dictionary: Dict[str, int]) -> List[int]:
    pns = []
    for text in texts:
        pn = [0]
        tokens = __get_tokens__(text)
        for token in tokens:
            if token not in dictionary:
                continue
            pn[0] += dictionary[token]
        if pn[0] == 0:
            pn[0] = 0
        elif pn[0] > 0:
            pn[0] = 1
        else:
            pn[0] = -1
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

def __get_model__() -> RandomForestClassifier:
    model = RandomForestClassifier(random_state=0)

    return model

def __create_mecab__() -> None:
    global mecab
    mecab = MeCab.Tagger()

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--dictionary_path', default='./pn.csv.m3.120408.trim')
    argument_parser.add_argument('--dataset_directory', default='./chABSA-dataset/')
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    __create_argument_parser__()
    train_by_dictionary(args.dictionary_path, args.dataset_directory, args.count_vectorizer_path, args.model_path)

if __name__ == '__main__':
    __main__()