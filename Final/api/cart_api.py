from components.connection import cart_collection


def setCart(user,products):
    res=cart_collection.find_one({'user':user})
    if res==None:
        cart_collection.insert_one({'user':user,'products':products})
    else:
        data=cart_collection.find_one({'user':user})['products']
        data.append(products[0])
        data=set(data)
        data=list(data)
        cart_collection.update_one({'user':user}, {"$set":{'products':data}})

def getCart(user):
    res=cart_collection.find_one({'user':user})
    if res==None:
        return []
    return res['products']