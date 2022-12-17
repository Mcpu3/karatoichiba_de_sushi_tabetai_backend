from typing import List

from predict_pns_by_dataset import predict_pns_by_dataset
from translate import translate_list


def predict(texts: List[str]) -> List[int]:
    translated_texts = translate_list('JA', 'EN', texts)
    predicted_pns = predict_pns_by_dataset(translated_texts)

    return predicted_pns

def __main__() -> None:
    texts_size = int(input('Texts size: '))
    texts = [input(f'Texts[{i}]: ') for i in range(texts_size)]
    predicted_pns = predict(texts)
    for text, predicted_pn in zip(texts, predicted_pns):
        print(text + ': ' + str(predicted_pn))

if __name__ == '__main__':
    __main__()