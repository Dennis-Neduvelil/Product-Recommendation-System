import pickle
import pandas as pd

content_model='models\content_based_model.pkl'

similarity= pickle.load(open(content_model, 'rb'))


df=pd.read_csv('models\data_content_based.csv')

print('Content Based Model Loaded')

def content_based_recommend(product,count):
    try:
        rec_list=[]
        product_index=df[df['id']==product].index[0]
        distances=similarity[product_index]
        product_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:count]
        for i in product_list:
            rec_list.append(df.iloc[i[0]].id)
        return rec_list
    except:
        return 'No Data'
