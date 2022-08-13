from components.connection import user_collection


def setUser(fname,lname,email,password):
    user_collection.insert_one({'fname':fname,'lname':lname,'email':email,'password':password})
    print('user Created')

def logUser(email,password):
    user=user_collection.find_one({'email':email,'password':password})
    if user==None:
        return 'no-user'
    else:
        return str(user['_id'])