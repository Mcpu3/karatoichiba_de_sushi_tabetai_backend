from argparse import ArgumentParser
import os
from pickle import dump
import sys
from typing import Dict

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm


def train_by_aclImdb(dataset_directory: str='./aclImdb/', count_vectorizer_path: str='./count_vectorizer.pickle', model_path: str='./model.pickle') -> None:
    print('Train', file=sys.stderr)
    dataset = __get_dataset__(dataset_directory, count_vectorizer_path)
    model = __get_model__()
    model.fit(dataset['x'], dataset['y'])
    with open(model_path, 'wb') as f:
        dump(model, f)

def __get_dataset__(dataset_directory: str, count_vectorizer_path: str) -> Dict:
    texts, pns = [], []
    with tqdm(os.listdir(os.path.join(dataset_directory, './train/pos/')), 'Get dataset') as pbar:
        for path in pbar:
            with open(os.path.join(dataset_directory, './train/pos/', path), encoding='utf-8') as f:
                text = f.readline()
                pn = 1
                texts.append(text)
                pns.append(pn)
            pbar.set_postfix({'path': os.path.join(dataset_directory, './train/pos/', path)})
    with tqdm(os.listdir(os.path.join(dataset_directory, './train/neg/')), 'Get dataset') as pbar:
        for path in pbar:
            with open(os.path.join(dataset_directory, './train/neg/', path), encoding='utf-8') as f:
                text = f.readline()
                pn = -1
                texts.append(text)
                pns.append(pn)
            pbar.set_postfix({'path': os.path.join(dataset_directory, './train/neg/', path)})
    with tqdm(os.listdir(os.path.join(dataset_directory, './test/pos/')), 'Get dataset') as pbar:
        for path in pbar:
            with open(os.path.join(dataset_directory, './test/pos/', path), encoding='utf-8') as f:
                text = f.readline()
                pn = 1
                texts.append(text)
                pns.append(pn)
            pbar.set_postfix({'path': os.path.join(dataset_directory, './test/pos/', path)})
    with tqdm(os.listdir(os.path.join(dataset_directory, './test/neg/')), 'Get dataset') as pbar:
        for path in pbar:
            with open(os.path.join(dataset_directory, './test/neg/', path), encoding='utf-8') as f:
                text = f.readline()
                pn = -1
                texts.append(text)
                pns.append(pn)
            pbar.set_postfix({'path': os.path.join(dataset_directory, './test/neg/', path)})
    count_vectorizer = CountVectorizer()
    bag_of_words = count_vectorizer.fit_transform(texts)
    with open(count_vectorizer_path, 'wb') as f:
        dump(count_vectorizer, f)
    x = bag_of_words
    y = pns
    dataset = {'x': x, 'y': y}

    return dataset

def __get_model__() -> RandomForestClassifier:
    # model = RandomForestClassifier(random_state=0)
    model = svm.LinearSVC(random_state=0)

    return model

def __create_argument_parser__() -> None:
    global args
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--dataset_directory', default='./aclImdb/')
    argument_parser.add_argument('--count_vectorizer_path', default='./count_vectorizer.pickle')
    argument_parser.add_argument('--model_path', default='./model.pickle')
    args = argument_parser.parse_args()

def __main__() -> None:
    __create_argument_parser__()
    train_by_aclImdb(args.dataset_directory, args.count_vectorizer_path, args.model_path)

if __name__ == '__main__':
    __main__()