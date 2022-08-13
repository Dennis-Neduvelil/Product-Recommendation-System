from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.flask_db

product_collection = db.Products
user_collection = db.User
cart_collection = db.Cart
purchase_collection = db.Purchase

print('DB Connected')