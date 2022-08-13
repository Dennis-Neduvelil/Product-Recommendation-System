from flask import Flask, render_template, request, make_response, redirect
from components.popularProducts import popular_recommend
from components.ContentBasedRec import content_based_recommend
# from components.collabrativeRec import collabrative_recommend
from components.imageRec import image_recommend
from api.products_api import getMultiple, getOneProduct
from api.auth_api import setUser, logUser
from api.cart_api import getCart, setCart
from api.purchase_api import setPurchase, getPurcahse
import shutil


def calCart(products):
    totalPrice = 0
    discPrice = 0
    profit = 0
    count = 0

    for i in products:
        totalPrice = totalPrice+i['price']
        discPrice = discPrice+i['discountedPrice']
        count += 1
    profit = totalPrice-discPrice
    return [count, totalPrice, profit, discPrice]


def userCheck():
    return request.cookies.get('userID')


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    user = userCheck()
    popular_products = popular_recommend(51)
    popular_products_data = getMultiple(popular_products)
    # collaborative_product_id=getPurcahse(user)
    # collaborative_products=collabrative_recommend(collaborative_product_id)
    # collaborative_products_data=getMultiple(collaborative_products)
    # print(collaborative_products_data)
    return render_template('home.html', popular_products=popular_products_data, user=user)


@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        user = userCheck()
        product_id = request.form['product_id']
        product_details = getOneProduct(product_id)
        product_id = int(product_id)
        content_rec = content_based_recommend(product_id, 40)
        if content_rec == 'No Data':
            content_based_products = 'No Data'
        else:
            content_based_products = getMultiple(content_rec)
    return render_template('product.html', product_details=product_details, content_based_products=content_based_products, user=user)


@app.route('/predict-style-upload', methods=['GET', 'POST'])
def predictStyleUpload():
    if request.method == 'POST':
        user = userCheck()
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save('static/predictImage.jpg')
            image_pred = image_recommend(6)
            image_pred_data = getMultiple(image_pred)
            print(image_pred_data)
        else:
            return 'Upload A Valid File'
    return render_template('imageRec.html', image_pred_data=image_pred_data, images=image_pred, user=user)


@app.route('/predict-style', methods=['GET', 'POST'])
def predictStyle():
    user = userCheck()
    pro_id = str(request.form['product'])
    source_loc = f'static\images\{pro_id}.jpg'
    shutil.copy(source_loc, 'static/predictImage.jpg')
    image_pred = image_recommend(6)
    image_pred_data = getMultiple(image_pred)
    print(image_pred_data)
    return render_template('imageRec.html', image_pred_data=image_pred_data, images=image_pred, user=user)


@app.route('/upload-file', methods=['GET'])
def uploadFile():
    user = userCheck()
    return render_template('upload-file.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = userCheck()
    if request.method == 'GET':
        return render_template('login.html', user=user)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        res = logUser(email, password)
        if res == 'no-user':
            return render_template('messege.html', message='Invalid Credentials !!!', message_desc='Either username or password is wrong,Go to the login screen and login to your account using correct credentials',btnname='Login',btnlink='/login')
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('userID', res)
            return resp


@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        user = userCheck()
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        setUser(fname, lname, email, password)
        return render_template('messege.html', message='Your Account is Created !!!', message_desc='Account creation completed, Now you can go to the login screen and login to your account',btnname='Login',btnlink='/login')


@app.route('/addtocart', methods=['GET', 'POST'])
def addtocart():
    if request.method == 'GET':
        user = userCheck()
        print(user)
        if user == None:
            return redirect('/login')
        else:
            cart = getCart(user)
            cartPro = getCart(user)
            cart_products_data = getMultiple(cartPro)
            cal = calCart(cart_products_data)

            return render_template('cart.html', cart=cart_products_data, cal=cal, proId=cartPro, user=user)

    if request.method == 'POST':
        user = userCheck()
        print(user)
        if user == None:
            return redirect('/login')
        else:
            products = request.form['product']
            setCart(user, [products])
            cartPro = getCart(user)
            cart_products_data = getMultiple(cartPro)
            cal = calCart(cart_products_data)
            return render_template('cart.html', cart=cart_products_data, cal=cal, proId=cartPro, user=user)


@app.route('/submitCart', methods=['GET', 'POST'])
def submitcart():
    if request.method == 'POST':
        user = userCheck()
        products = request.form['cartItems']
        setPurchase(user, products)
        return render_template('messege.html', message='Purchase Completed', message_desc='your purchase is completed, now you can go to the home',btnname='Go Home',btnlink='/')


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('userID')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
