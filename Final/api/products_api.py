import lxml
import ast
from bs4 import BeautifulSoup
from components.connection import product_collection


def getMultiple(arr):
    items_list=[]
    for i in arr:
        id=int(i)
        data=product_collection.find_one({'id':id},{'id','productDisplayName','price','discountedPrice'})
        items_list.append(data)
    return items_list

def getOneProduct(id):
    id=int(id)
    data=product_collection.find_one({'id':id},{'id','productDisplayName','price','discountedPrice','variantName','brandName','ageGroup','gender','baseColour','usage','productDescriptors'})
    return data
    

