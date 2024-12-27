from app import app
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import request
import socket
from flask_login import UserMixin

# Get the current machine's hostname
hostname = socket.gethostname()
print("hostname",hostname,hostname == 'DESKTOP-6FGNSTO')

if hostname == 'DESKTOP-6FGNSTO' or hostname == 'your-local-machine-name':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/avke'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Billion%4023@localhost/avkenew'


current_path = os.getcwd()  # Or use __file__ if checking within a specific file
# Check if '/var/' is in the path
# Removed var check in current path as getcwd producing / as the result
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/avke'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Billion%4023@localhost/avkenew'


# @app.route('/viewdbstatus')
# def viewdbstatus():
#     return app.config['SQLALCHEMY_DATABASE_URI']+" -- Path:"+current_path


db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    highlights = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    # category_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), unique=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), unique=False)
    sub_sub_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), unique=False)

    # Relationships
    category = db.relationship('Category', foreign_keys=[category_id], backref='products_main')
    sub_category = db.relationship('Category', foreign_keys=[sub_category_id], backref='products_sub')
    sub_sub_category = db.relationship('Category', foreign_keys=[sub_sub_category_id], backref='products_sub_sub')
    
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, nullable=False)
    # customer_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    order_details = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
        # Set up relationship
    # customer = db.relationship('Customer', backref='orders')

# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False)
#     websitename = db.Column(db.Text, nullable=False)
#     websitevisits = db.Column(db.Integer, nullable=False)
#     phone = db.Column(db.Text, nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
#     updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    websitename = db.Column(db.Text, nullable=False)
    websitevisits = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    order = db.relationship('Order', backref='user', uselist=False)
    payment = db.relationship('Payment', backref='user', uselist=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

    def __init__(self, name, websitename, websitevisits,password, phone, email):
        self.name = name
        self.websitename = websitename
        self.websitevisits = websitevisits
        self.phone = phone
        self.password = password
        self.email = email

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    order = db.relationship('Order', backref='customer', uselist=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Text, nullable=False)
    total = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    status = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)



class Category(db.Model):
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    parent_category_id = db.Column(db.Integer, unique=True)
    # product = db.relationship('Product', backref='category', uselist=False)
        # Relationship to establish parent-child hierarchy
    parent = db.relationship('Category', remote_side=[id], backref='children')
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.title}>'
