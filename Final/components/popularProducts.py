import pickle

popular_model='models\popular_model.pkl'

popular_clf= pickle.load(open(popular_model, 'rb'))

print('Popular Model Loaded')

def popular_recommend(value):
    return list(popular_clf[0:value].id)


