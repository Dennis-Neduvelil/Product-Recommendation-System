import pickle
import pandas as pd
import numpy as np

collabrative_model='models\collabrative_filtering_model.pkl'

model= pickle.load(open(collabrative_model, 'rb'))

df=pd.read_csv('models\pivot_table_transactions.csv')

print('Collaborative Model Loaded')

def collabrative_recommend(product_id):
    index=np.where(df.Products==product_id)[0][0]
    similar_items = sorted(list(enumerate(model[0])),key=lambda x:x[1],reverse=True)[1:21]
    for i in similar_items:
        print(df.Products[i[0]])

collabrative_recommend(1163)