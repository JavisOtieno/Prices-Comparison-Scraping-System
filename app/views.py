from app import app
from flask import render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import os
from .models import Product  # Import Product model
from .models import Order
from .models import Category


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
    return render_template("public/home.html")



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

@app.route('/products')
def showProducts():
    data = Product.query.all()
    productString = ""
    for product in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
         formatted_price = "{:,}".format(int(product.price))
         productString=productString+str(product.name)+" "+str(formatted_price)+" "+str(product.description)+" "+str(product.created_at)+"<br/>"
    return productString



@app.route('/categories')
def showCategories():
    data = Category.query.all()
    categoryString = ""
    for category in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
        #  formatted_price = "{:,}".format(int(product.price))
         categoryString=categoryString+str(category.name)+" "+"<br/>"
    return categoryString

@app.route('/categories')
def categoriesRender():
    data = Category.query.all()
    categoryString = ""
    for category in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
        #  formatted_price = "{:,}".format(int(product.price))
         categoryString=categoryString+str(category.name)+" "+"<br/>"
    return render_template('admin/categories.html', categories=categoryString)

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
    data = Order.query.all()
    orderString = ""
    for order in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
         formatted_total = "{:,}".format(int(order.total))
         orderString=orderString+str(order.user_id)+" "+str(formatted_total)+" "+str(order.notes)+" "+str(order.created_at)+"<br/>"
    return render_template('orders.html', categories=orderString)

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