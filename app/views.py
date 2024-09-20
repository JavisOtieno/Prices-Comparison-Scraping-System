from app import app
from flask import render_template,request,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import os
from .models import Product  # Import Product model
from .models import Order
from .models import Category
from .models import User
from .models import Payment
from .models import Customer
from .models import db

current_path = os.getcwd() 
@app.route('/viewdbstatus')
def viewdbstatus():
    return app.config['SQLALCHEMY_DATABASE_URI']+" -- Path:"+current_path

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/products'
# db = SQLAlchemy(app)

# class Product(db.Model):
#     __tablename__ = 'products'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255),nullable=False)
#     price = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.TIMESTAMP, nullable=True, default=None)
#     updated_at = db.Column(db.TIMESTAMP, nullable=True, default=None)

@app.route('/')
def index():
    return render_template('index.html')



#Load the model

# model_path='model.pkl'





@app.route('/predict', methods=['POST'])
def predict():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    #    return model_path
    # Get input values from form
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]

    # Make prediction
    prediction = model.predict(final_features)
    #prediction = [2,1,32,32]
    output = prediction[0]
    

    return render_template('public/result.html', prediction_text=f'Predicted class: {output}')

@app.route('/createproduct', methods=['GET', 'POST'])
def createproduct():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        commission = request.form['commission']
        cost = request.form['cost']
        image = request.form['image']
        status = request.form['status']
        description = request.form['description']
        product = Product(name=name, price=price,
                          commission=commission,image=image,
                          cost=cost,
                          status=status,description=description)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('indexproducts'))
    return render_template('product/create.html')

# Update record
@app.route('/editproduct/<int:id>', methods=['GET', 'POST'])
def editproduct(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.commission = request.form['commission']
        product.cost = request.form['cost']
        product.image = request.form['image']
        product.status = request.form['status']
        product.description = request.form['description']
        db.session.commit()
        return redirect(url_for('indexproducts'))
    return render_template('product/edit.html', product=product)

@app.route('/products')
def indexproducts():
    products = Product.query.all()
    return render_template('product/index.html', products=products)

# Delete record
@app.route('/deleteproduct/<int:id>')
def deleteProduct(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('indexproducts'))


# @app.route('/products')
# def showProducts():
#     products = Product.query.all()
#     return render_template('products.html', 
#     products=products)

@app.route('/payments')
def showPayments():
    payments = Payment.query.all()
    return render_template('payments.html', 
    payments=payments)

@app.route('/customers')
def showCustomers():
    customers = Customer.query.all()
    return render_template('customers.html', 
    customers=customers)



@app.route('/categories')
def categoriesRender():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/dashboard')
def dashboard():
    data = Category.query.all()
    categoryString = ""
    for category in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
        #  formatted_price = "{:,}".format(int(product.price))
         categoryString=categoryString+str(category.name)+" "+"<br/>"
    return render_template('index.html', categories=categoryString)

@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/logout')
def logout():
    #implement logout
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')






@app.route('/about')
def about():
    return "<h1>About</h1>"