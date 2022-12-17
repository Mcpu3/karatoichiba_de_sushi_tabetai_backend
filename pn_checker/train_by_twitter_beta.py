from argparse import ArgumentParser
import csv
from pickle import dump
import sys
from typing import Dict, List, Generator

import pyinflect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
import spacy


def train_by_twitter(dataset_path: str='./training.1600000.processed.noemoticon.csv', count_vectorizer_path: str='./count_vectorizer.pickle', model_path: str='./model.pickle') -> None:
    print('Train', file=sys.stderr)
    __create_spacy__()
    dataset = __get_dataset__(dataset_path, count_vectorizer_path)
    model = __get_model__()
    model.fit(dataset['x'], dataset['y'])
    with open(model_path, 'wb') as f:
        dump(model, f)

def __get_dataset__(dataset_path: str, count_vectorizer_path: str) -> Dict:
    texts, pns = [], []
    with open(dataset_path, encoding='ISO-8859-1') as f:
        raw = csv.reader(f)
        for row in raw:
            text = row[5]
            if int(row[0]) == 0:
                pn = -1
            elif int(row[0]) == 4:
                pn = 1
            else:
                continue
            texts.append(text)
            pns.append(pn)
    count_vectorizer = CountVectorizer(tokenizer=__get_tokens__, ngram_range=(1, 2))
    bag_of_words = count_vectorizer.fit_transform(texts)
    with open(count_vectorizer_path, 'wb') as f:
        dump(count_vectorizer, f)
    x = bag_of_words
    y = pns
    dataset = {'x': x, 'y': y}

    return dataset

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

def __get_model__() -> LinearSVC:
    model = LinearSVC(random_state=0)

    return model

def __create_spacy__() -> None:
    global nlp
    nlp = spacy.load('en_core_web_sm')

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--dataset_path', default='./training.1600000.processed.noemoticon.csv')
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    __create_argument_parser__()
    train_by_twitter(args.dataset_path, args.count_vectorizer_path, args.model_path)

if __name__ == '__main__':
    __main__()