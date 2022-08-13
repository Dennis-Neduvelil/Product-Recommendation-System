from components.connection import purchase_collection
from components.connection import cart_collection


def setPurchase(user,products):
    value=products

    value= value.replace('"', '')
    value= value.replace('[', '')
    value= value.replace(']', '')
    value= value.replace("'", '')

    products=list(map(int,value.split(',')))

    res=purchase_collection.find_one({'user':user})
    if res==None:
        purchase_collection.insert_one({'user':user,'products':products})
        cart_collection.update_one({'user':user}, {"$set":{'products':[]}})
    else:
        data=purchase_collection.find_one({'user':user})['products']
        data.append(products[0])
        data=set(data)
        data=list(data)
        purchase_collection.update_one({'user':user}, {"$set":{'products':data}})
        cart_collection.update_one({'user':user}, {"$set":{'products':[]}})
 
def getPurcahse(user):
    data=purchase_collection.find_one({'user':user})['products']
    return data[0]


