from app import app
from flask import render_template,request,redirect,url_for, session
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

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# import secrets

# secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string
# print('secret ',secret_key)
# app = Flask(__name__)
app.secret_key = 'f735e47866cceca5cc3113cab5d2b58b'


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Route to redirect if login is required



# Dummy user database
users = {'test_user': 'password123'}

# Define how to load a user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # users = {'test_user@gmail.com': 'password123'}
        email = request.form['email']
        password = request.form['password']
        # return(email," - ",password)
        user = User.query.filter_by(email=email).first()


        if user:
        # and user[email] == password:
            # user = User(email)
            login_user(user)
            return redirect(url_for('index'))
        # return 'Invalid credentials'
        return redirect(url_for('login'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Protected route - requires login
@app.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.id}! You are logged in.'

# if __name__ == '__main__':
#     app.run(debug=True)


current_path = os.getcwd()
@login_required 
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
@login_required
def index():
    return render_template('index.html')



#Load the model

# model_path='model.pkl'





@app.route('/predict', methods=['POST'])
@login_required
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


@app.route('/createorder', methods=['GET', 'POST'])
@login_required
def createorder():
    if request.method == 'POST':
        user_id =request.form['user_id']
        customer_id = request.form['customer_id']
        value = request.form['value']
        notes = request.form['notes']
        status = request.form['status']
        cart_id = request.form['cart_id']
        order = Order(user_id=user_id, customer_id=customer_id,
                          value=value,notes=notes,
                          cart_id=cart_id,status=status)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('indexorders'))
    return render_template('order/create.html')

# Update record
@app.route('/editorder/<int:id>', methods=['GET', 'POST'])
@login_required
def editorder(id):
    order = Order.query.get(id)
    if request.method == 'POST':
        order.user_id =request.form['user_id']
        order.customer_id = request.form['customer_id']
        order.value = request.form['value']
        order.notes = request.form['notes']
        order.status = request.form['status']
        order.cart_id = request.form['cart_id']
        db.session.commit()
        return redirect(url_for('indexorders'))
    return render_template('order/edit.html', order=order)

@app.route('/orders')
@login_required
def indexorders():
    orders = Order.query.all()
    return render_template('order/index.html', orders=orders)

# Delete record
@app.route('/deleteorder/<int:id>')
@login_required
def deleteOrder(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('indexorders'))


@app.route('/createproduct', methods=['GET', 'POST'])
@login_required
def createproduct():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        commission = request.form['commission']
        cost = request.form['cost']
        image = request.form['image']
        status = request.form['status']
        highlights = request.form['highlights']
        description = request.form['description']
        product = Product(name=name, price=price,
                          commission=commission,image=image,
                          cost=cost,highlights=highlights,
                          status=status,description=description)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('indexproducts'))
    return render_template('product/create.html')

# Update record
@app.route('/editproduct/<int:id>', methods=['GET', 'POST'])
@login_required
def editproduct(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.commission = request.form['commission']
        product.cost = request.form['cost']
        product.image = request.form['image']
        product.status = request.form['status']
        product.highlights = request.form['highlights']
        product.description = request.form['description']
        db.session.commit()
        return redirect(url_for('indexproducts'))
    return render_template('product/edit.html', product=product)

@app.route('/products')
@login_required
def indexproducts():
    products = Product.query.all()
    return render_template('product/index.html', products=products)

# Delete record
@app.route('/deleteproduct/<int:id>')
@login_required
def deleteProduct(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('indexproducts'))



@app.route('/create', methods=['GET', 'POST'])
# def create():
#     form = StudentForm()
#     if form.validate_on_submit():
#         # Save to database (replace this with your logic)
#         flash('Category created successfully!', 'success')
#         return redirect(url_for('indexcategories'))
#     return render_template('category/create.html', form=form)
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('indexcategories'))
    return render_template('category/create.html')

# Update record
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get(id)
    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()
        return redirect(url_for('indexcategories'))
    return render_template('category/edit.html', category=category)

@app.route('/categories')
@login_required
def indexcategories():
    categories = Category.query.all()
    return render_template('category/index.html', categories=categories)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('indexcategories'))

@app.route('/createpayment', methods=['GET', 'POST'])
@login_required
def createpayment():
    if request.method == 'POST':
        total = request.form['total']
        user_id = request.form['user_id']
        payment = Payment(total=total,user_id=user_id)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('indexpayments'))
    return render_template('payment/create.html')

# Update record
@app.route('/editpayment/<int:id>', methods=['GET', 'POST'])
@login_required
def editpayment(id):
    payment = Payment.query.get(id)
    if request.method == 'POST':
        payment.total = request.form['total']
        payment.user_id = request.form['user_id']
        db.session.commit()
        return redirect(url_for('indexpayments'))
    return render_template('payment/edit.html', payment=payment)



@app.route('/payments')
@login_required
def indexpayments():
    payments = Payment.query.all()
    return render_template('payment/index.html', payments=payments)

@app.route('/deletepayment/<int:id>')
@login_required
def deletepayment(id):
    payment = Payment.query.get(id)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for('indexpayments'))

# @app.route('/products')
# def showProducts():
#     products = Product.query.all()
#     return render_template('products.html', 
#     products=products)

@app.route('/payments')
@login_required
def showPayments():
    payments = Payment.query.all()
    return render_template('payments.html', 
    payments=payments)

@app.route('/customers')
@login_required
def showCustomers():
    customers = Customer.query.all()
    return render_template('customers.html', 
    customers=customers)



@app.route('/categories')
@login_required
def categoriesRender():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/dashboard')
@login_required
def dashboard():
    data = Category.query.all()
    categoryString = ""
    for category in data:
         #formatted_price = locale.format_string("%d", product.price, grouping=True)
        #  formatted_price = "{:,}".format(int(product.price))
         categoryString=categoryString+str(category.name)+" "+"<br/>"
    return render_template('index.html', categories=categoryString)

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# @app.route('/logout')
# def logout():
#     #implement logout
#     return redirect(url_for('login'))

# @app.route('/login')
# def login():
#     return render_template('login.html')






@app.route('/about')
@login_required
def about():
    return "<h1>About</h1>"