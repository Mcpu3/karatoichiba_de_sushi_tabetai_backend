from pn_predictor.predict_pns import predict_pns

texts_size = int(input('Texts size: '))
texts = [input(f'Texts[{i}]: ') for i in range(texts_size)]
predicted_pns = predict_pns(texts, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
for text, predicted_pn in zip(texts, predicted_pns):
    print(text + ': ' + str(predicted_pn))