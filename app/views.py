from app import app
from flask import render_template,request,redirect,url_for,session,flash,make_response,jsonify
# from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import os
import re
from .models import Product  # Import Product model
from .models import Order
from .models import Category
from .models import User
from .models import Payment
from .models import Customer
from .models import Productlink
from .models import db
import bcrypt
from sqlalchemy import func
from datetime import datetime
from werkzeug.utils import secure_filename
import pdfkit
from bs4 import BeautifulSoup
import requests
import html
from sqlalchemy.sql import extract
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import socket

# Configure path to wkhtmltopdf
# path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'  # Adjust for your system
path_to_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'


# Define paths for wkhtmltopdf
local_path_to_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
production_path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'

hostname = socket.gethostname()
print("hostname",hostname,hostname == 'DESKTOP-6FGNSTO')


# Assuming your development environment is 'localhost' or starts with something specific
if hostname == 'DESKTOP-6FGNSTO' or hostname == 'your-local-machine-name':
    path_to_wkhtmltopdf = local_path_to_wkhtmltopdf
else:
    path_to_wkhtmltopdf = production_path_to_wkhtmltopdf

pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Get environment
# environment = os.getenv('ENVIRONMENT', 'development')  # default to 'development' if not set

# if environment == 'development':
#     path_to_wkhtmltopdf = local_path_to_wkhtmltopdf
# else:
#     path_to_wkhtmltopdf = production_path_to_wkhtmltopdf

# pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# import secrets

# secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string
# print('secret ',secret_key)
# app = Flask(__name__)
app.secret_key = 'f735e47866cceca5cc3113cab5d2b58b'


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Route to redirect if login is required

# Define the folder where you want to save uploaded images
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Add the upload folder to your Flask configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')


# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Dummy user database
users = {'test_user': 'password123'}

# Define how to load a user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/productlinks')
def indexproductlinks():
    productlinks = Productlink.query.all()
    # Format the data for response
    # Create a plain text response
    # response = "\n".join([f"link: '{pl.link}' - price: '{pl.price}'" for pl in productlinks])
    return render_template('link/index.html', links=productlinks)
    # return render_template('category/index.html', categories=categories)

@app.route('/testscrape')
@login_required
def test_scrape():
    # URL of the product page
    url = 'https://starmac.co.ke/product/jbl-bar-1300x/'
    # Fetch the HTML content of the page
    response = requests.get(url)
    html_content = response.content
    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the price element
    price_element = soup.find('p', class_='price')
    # Extract the numeric value
    
    #test create link
    # productlink = Productlink(link='https://starmac.co.ke/product/jbl-bar-1300x/',
    #                           price='150000',]
    #                       )
    # db.session.add(productlink)
    # db.session.commit()
    
    
    
    if price_element:
        price_text = price_element.get_text(strip=True)
        # Remove the currency symbol and formatting to keep only the numeric value
        price_value = price_text.replace('KShs', '').replace(',', '').replace('.00', '').strip()
        return(f"Price Value: {price_value}")
    else:
        return("Price not found.")
    
    
@app.route('/scrapelisturls', methods=['GET', 'POST'])
@login_required
def extract_product_links():
    if request.method == 'POST':
        page_number = int(request.form['page_number'])
        base_url = request.form['url'].rstrip('/')  # Ensure no trailing slash
        all_product_links = []
        upper_page_limit = page_number +int(request.form['upper_page_limit'])
        page_number_increments = ''

        while (page_number < upper_page_limit):
        # while True:        # Construct the URL for the current page
            url = f"{base_url}/shop/page/{page_number}"
            
            response = requests.get(url)
            html_content = response.content
            # return html_content
            # Parse the HTML with Beautiful Soup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all product divs
            product_links = []
            for product_div in soup.find_all('div', class_='product-grid-item'):
                # Locate the <a> tag within the div
                # return html.escape(str(product_div))
                link_tag = product_div.find('a', class_='product-image-link')
                product_name = product_div.find('h3', class_='wd-entities-title').text.strip()
                if not product_name:
                    product_name=''
                product_price_org = product_div.find('div', class_='wrap-price').get_text(strip=True)
                try:
                    price_value = product_price_org.replace('KShs',
                    '').replace(',', '').replace('.00',
                    '').replace('KSh','').strip()
                    product_price = float(price_value)
                except ValueError:
                    product_price = 0
                if link_tag and 'href' in link_tag.attrs:
                    newlink = link_tag['href']
                    product_links.append({'link': newlink, 'price': html.escape(str(product_price_org)), 
                                          'name': product_name})
                    productlink = Productlink.query.filter_by(link=newlink).first()
                    if not productlink:
                        # Create a new Productlink entry
                        new_productlink = Productlink(name=product_name,link=newlink,price=product_price)
                        db.session.add(new_productlink)
                        # db.session.commit()
                    else:
                        productlink.price = product_price
                    db.session.commit()



            # If no product links are found, break the loop
            if not product_links:
                break
            
            # Add the links from the current page to the total list
            all_product_links.extend(product_links)

            # Increment page number for the next iteration
            page_number = page_number + 1
            page_number_increments = page_number_increments+' - '+page_number
        return page_number_increments+"<br>".join([f"{item['link']}: {item['name']} : {item['price']}" for item in product_links])

        # Return all the product links as a string
        # Create an array to store the prices
        product_prices = []

        # Loop through the product links to fetch prices
        for link in all_product_links[:5]:
            # headers = {
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            # }
            response2 = requests.get(link)
            # response2 = requests.get(link)
            html_content_2 = response2.content
            productlink = Productlink.query.filter_by(link=link).first()
            # return html_content_2
            # if not productlink:
            #     productlink = Productlink(link=link,price=0)
            #     db.session.add(productlink)
            #     db.session.commit()

            # Parse the HTML with Beautiful Soup
            soup2 = BeautifulSoup(html_content_2, 'html.parser')

            # Find the price element
            price_element = soup2.find('p', class_='price')

            # Extract the numeric value
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Remove the currency symbol and formatting to keep only the numeric value
                price_value = price_text.replace('KShs',
                '').replace(',', '').replace('.00',
                '').replace('KSh','').strip()
                product_prices.append({'link': link, 'price': price_value})
                try:
                    price_value = float(price_value)
                except ValueError:
                    price_value = 0
                product_title = soup.select_one('.product_title.entry-title')
                if not product_title:
                    # print("Product Name:", product_title.text.strip())
                    product_title = ''
                # order.cart_id = request.form['cart_id']
                if not productlink:
                    productlink = Productlink(name=product_title,link=link, price=price_value)
                    db.session.add(productlink)
                else:
                    productlink.price = price_value
                db.session.commit()
            else:
                product_prices.append({'link': link, 'price': 'Price not found'})

        # Return the product prices as a string
        return "<br>".join([f"{item['link']}: {item['price']}" for item in product_prices])
    return render_template('scrape/scrapeurl.html')

# Call the function
# product_links = extract_product_links()
# print(product_links)

@app.route('/addproductfromlink/<int:id>')
@login_required
def addproductfromlink(id):
        link = Productlink.query.get(id)
        # Fetch the HTML content of the page
        response2 = requests.get(link.link)
        # response2 = requests.get(link)
        html_content_2 = response2.content
        # productlink = Productlink.query.filter_by(link=link).first()
        # return html_content_2
        # if not productlink:
        #     productlink = Productlink(link=link,price=0)
        #     db.session.add(productlink)
        #     db.session.commit()

        # Parse the HTML with Beautiful Soup
        soup2 = BeautifulSoup(html_content_2, 'html.parser')

        # Find the price element
        price_element = soup2.find('p', class_='price')

        # Extract the numeric value
        if price_element:
            price_text = price_element.get_text(strip=True)
            # Remove the currency symbol and formatting to keep only the numeric value
            price_value = price_text.replace('KShs',
            '').replace(',', '').replace('.00',
            '').replace('KSh','').strip()
            #product_prices.append({'link': link, 'price': price_value})
            try:
                price_value = float(price_value)
            except ValueError:
                price_value = 0
            product_title = soup2.select_one('.product_title.entry-title')
            short_description = soup2.select_one('.woocommerce-product-details__short-description')
            main_description = soup2.select_one('.wd-single-content')
            # image = soup2.select_one('.woocommerce-product-gallery__image0')
            # image_url = image['data_thumb']
            og_image_tag = soup2.find('meta', property='og:image')
    
            # Extract the image URL
            if og_image_tag:
                image_url = og_image_tag.get('content')

            if not product_title:
                # print("Product Name:", product_title.text.strip())
                product_title = ''
            else: 
                product_title = product_title.text.strip()
            if not image_url:
                # print("Product Name:", product_title.text.strip())
                image_url = ''
 
                
            if not short_description:
                # print("Product Name:", product_title.text.strip())
                short_description = ''
            else:
                short_description =  str(short_description)
                
            if not main_description:
                # print("Product Name:", product_title.text.strip())
                main_description = ''
            else:
                    # Remove all <a> tags
                for a_tag in main_description.find_all("a"):
                    a_tag.replace_with(a_tag.text)
                
                # Remove all <img> tags
                for img_tag in main_description.find_all("img"):
                    img_tag.decompose()
            main_description = str(main_description).replace("Starmac Kenya", "our store")
            main_description = str(main_description).replace("Starmac", "our store")
        
                # main_description = main_description.text.strip()
            # order.cart_id = request.form['cart_id']
            breadcrumb_nav = soup2.find('nav', class_='wd-breadcrumbs woocommerce-breadcrumb')
            categories = [a.get_text() for a in breadcrumb_nav.find_all('a')]
            categories = categories[1:]
            
            sub_category_id = None
            sub_sub_category_id = None
            parent_category_id = None
            
            for category in categories:
                index_of_current_category = categories.index(category)
            # Check if the category exists in the table
                category_title = category.strip()
                category = category_title.lower()
                formatted_category_name = category.replace(" ", "_")
                formatted_category_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', formatted_category_name)
                categorydetected = Category.query.filter_by(name=formatted_category_name).first()
                
            
                if categorydetected:
                    
                    if index_of_current_category == 0:
                        main_category_id = categorydetected.id
                    
                        
                    elif index_of_current_category == 1:
                        sub_category_id = categorydetected.id
                        
                    elif index_of_current_category == 2:
                        sub_sub_category_id = categorydetected.id
                    else: 
                        break
                    parent_category_id =categorydetected.id
                    # print(f"Category '{category}' exists. Assigning category ID {category_id} to product {product_id}.")
                else:
                    # If it doesn't exist, create a new category and assign it
                    # category_id = create_category_and_assign_product(category)
                    name = formatted_category_name
                    parent_category_id = parent_category_id
                    title = category_title
                    
                    if index_of_current_category == 0:
                        type = 'main'
                    elif index_of_current_category == 1:
                        type = 'sub'    
                    elif index_of_current_category == 2:
                        type = 'subsub'
                    else: 
                        break
                    
                    
                    categorysaved = Category(name=formatted_category_name,title=category_title,parent_category_id=parent_category_id,type=type)
                    db.session.add(categorysaved)
                    db.session.commit()
                    parent_category_id = categorysaved.id
                    
                    
                    
                    
                    if index_of_current_category == 0:
                        main_category_id = categorysaved.id
                        
                    elif index_of_current_category == 1:
                        sub_category_id = categorysaved.id
                    else:
                        sub_sub_category_id = categorysaved.id
                    
                    # print(f"Category '{category}' created. Assigning category ID {category_id} to product {product_id}.")
                
           
                    
            name = product_title
            price = price_value
            commission = price_value*5/100
            cost = 0
            image = image_url
            category_id = main_category_id
            sub_category_id = sub_category_id
            sub_sub_category_id = sub_sub_category_id
            status = 'available'
            highlights = short_description
            description = main_description
            
            response = requests.get(image_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Set the file path where the image will be saved
                formatted_name = product_title.lower()
                    
                    # Replace spaces with underscores
                formatted_name = formatted_name.replace(" ", "_")
                formatted_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', formatted_name)
                file_name = formatted_name+".jpg"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)  # Replace "path_to_your_directory" with the actual path

                # Write the image to a file
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                image_savedurl = url_for('static', filename=f'uploads/{file_name}')
                # print(f"Image saved successfully at {file_path}")
                
            else:
                image_savedurl = ''
            
            product_data = {
            "name": product_title,
            "price": price_value,
            "commission": price_value * 5 / 100,  # 5% commission
            "image": image_savedurl,
            "category_id": category_id,
            "sub_category_id": sub_category_id,
            "sub_sub_category_id": sub_sub_category_id,
            "cost": 0,
            "highlights": short_description,
            "status": "available",
            "description": short_description
            }
            
            product = Product(name=name, price=price,
                        commission=commission,image=image_savedurl,
                        category_id=category_id,sub_category_id=sub_category_id,
                        sub_sub_category_id=sub_sub_category_id,
                        cost=cost,highlights=highlights,
                        status=status,description=description)
            # return jsonify(product_data)
            db.session.add(product)
            db.session.commit()
            link.product_id = product.id
            
            db.session.commit()
            return jsonify(product_data)
            

@app.route('/raise_error')
def raise_error():
    try:
        # Simulate an error
        raise Exception("Something went wrong in the view!")
    except Exception as e:
        return render_template('error.html', error_message=str(e)), 500

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
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
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
    productlinkcount = Productlink.query.count()
    order_count = Order.query.count()
    user_count = User.query.count()
    customer_count = Customer.query.count()
    product_count = Product.query.count()

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Query the total number of orders or total sales for the current month
    # Example 1: Count total orders for the current month
    orders_this_month = Order.query.filter(
        func.extract('year', Order.created_at) == current_year,
        func.extract('month', Order.created_at) == current_month
    ).count()
    

    productlink_count_month = Product.query.filter(
        func.extract('year', Product.created_at) == current_year,
        func.extract('month', Product.created_at) == current_month
    ).count()
    
    
    # start_of_week = now - timedelta(days=now.weekday())

    # productlink_count_week = Productlink.query.filter(
    #     Productlink.created_at >= start_of_week
    # ).count()
    # productlink_count_week = Product.query.filter(
    #     func.extract('year', Product.created_at) == current_year,
    #     func.extract('month', Product.created_at) == current_month
    # ).count()
    
    productlink_count_day = Productlink.query.filter(
    func.date(Productlink.created_at) == func.current_date()
    ).count()
    
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)  # Sunday end

    # Query products created this week
    productlink_count_week = Product.query.filter(
        Product.created_at >= start_of_week,
        Product.created_at <= end_of_week
    ).count()

        # Example 1: Count total orders for the current month
    products_this_month = Product.query.filter(
        func.extract('year', Product.created_at) == current_year,
        func.extract('month', Product.created_at) == current_month
    ).count()

        # Example 1: Count total orders for the current month
    customers_this_month = Customer.query.filter(
        func.extract('year', Customer.created_at) == current_year,
        func.extract('month', Customer.created_at) == current_month
    ).count()

        # Example 1: Count total orders for the current month
    users_this_month = User.query.filter(
        func.extract('year', User.created_at) == current_year,
        func.extract('month', User.created_at) == current_month
    ).count()

    links = Productlink.query.order_by(Productlink.created_at.desc()).limit(10).all()

    return render_template('index.html', productlinkcount = productlinkcount,
                           user_count=user_count, productlink_count_month=productlink_count_month,
                           productlink_count_week=productlink_count_week,
                           productlink_count_day=productlink_count_day,
                           order_count=order_count,
                           customer_count=customer_count,product_count=product_count,
                           products_this_month=products_this_month,
                           orders_this_month=orders_this_month,
                           customers_this_month=customers_this_month,
                           users_this_month=users_this_month, links=links)



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
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        customer_delivery_location = request.form['customer_delivery_location']
        customer = Customer(name=customer_name, phone=customer_phone,
                          email='',)
        db.session.add(customer)
        db.session.commit()
        customer_id = customer.id
        value = request.form['value']
        order_details = request.form['order_details']
        notes = request.form['notes']
        status = request.form['status']
        # cart_id = request.form['cart_id']
        quantity = 1
        order = Order(user_id=user_id, customer_id=customer_id,
                      order_details=order_details,
                        value=value,notes=notes, quantity=quantity,status=status)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('indexorders'))
    users = User.query.all()
    return render_template('order/create.html',users=users)

# Update record
@app.route('/editorder/<int:id>', methods=['GET', 'POST'])
@login_required
def editorder(id):
    order = Order.query.get(id)
    if request.method == 'POST':
        order.user_id =request.form['user_id']
        order.customer_id = request.form['customer_id']
        order.order_details = request.form['order_details']
        order.value = request.form['value']
        order.notes = request.form['notes']
        order.status = request.form['status']
        # order.cart_id = request.form['cart_id']
        db.session.commit()
        return redirect(url_for('indexorders'))
    users = User.query.all()
    return render_template('order/edit.html', order=order,users=users)

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

@app.route('/invoice/<int:customer_id>')
def view_invoice(customer_id):
    # Fetch customer data from your model
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return "Customer not found", 404

    # Render the HTML template with customer data
    return render_template('invoice/index.html', customer=customer)

@app.route('/pdf/view/<int:customer_id>')
def view_pdf(customer_id):
    # Fetch customer data from your model
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return "Customer not found", 404

    # Render the HTML template with customer data
    rendered_html = render_template('invoice/index.html', customer=customer)

    # Generate PDF from the rendered HTML
    # pdf = pdfkit.from_string(rendered_html, False, configuration=pdfkit_config)

    pdf = pdfkit.from_string(rendered_html, False, configuration=pdfkit_config, options={
        'enable-local-file-access': '',
    'no-stop-slow-scripts': '',
        'zoom': '1.3',
        'dpi': 300,
        'no-outline': None,
        'print-media-type': ''
    })

    # Return the PDF to be displayed in the browser
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response


@app.route('/pdf/<int:customer_id>')
def generate_pdf(customer_id):
    # Fetch customer data from your model
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return "Customer not found", 404

    # Render the HTML template with customer data
    rendered_html = render_template('invoice/index.html', customer=customer)

    # Generate PDF from the rendered HTML
    pdf = pdfkit.from_string(rendered_html, False, configuration=pdfkit_config)

    # Return the PDF as a downloadable response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=customer_{customer.id}.pdf'
    return response


@app.route('/createproduct', methods=['GET', 'POST'])
@login_required
def createproduct():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        commission = request.form['commission']
        cost = request.form['cost']
        image = request.form['image']
        category_id = request.form['category_id']
        sub_category_id = request.form['sub_category_id']
        sub_sub_category_id = request.form['sub_sub_category_id']
        status = request.form['status']
        highlights = request.form['highlights']
        description = request.form['description']
        


                # Handle the uploaded image
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image = request.files['image']

        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
                # Ensure the upload directory exists
        # if not os.path.exists(app.config['UPLOAD_FOLDER']):
        #     os.makedirs(app.config['UPLOAD_FOLDER'])

        if image and allowed_file(image.filename):
            # Secure the filename and save the file
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # file_path = os.path.join(upload_folder, filename)
            # file.save(file_path)

            image_url = url_for('static', filename=f'uploads/{filename}')

            product = Product(name=name, price=price,
                            commission=commission,image=image_url,
                            category_id=category_id,sub_category_id=sub_category_id,
                            sub_sub_category_id=sub_sub_category_id,
                            cost=cost,highlights=highlights,
                            status=status,description=description)
            db.session.add(product)
            db.session.commit()

            # Save the image URL to the database
            # new_product = Product(image_url=image_url)

            # Save product details and image filename to the database
            # Example: new_product = Product(name=name, price=price, image=filename, ...)
            
            # Perform further actions, like saving product to the database

            flash('Product created successfully!')
            # return redirect(url_for('products'))

        flash('Invalid file format')


        return redirect(url_for('indexproducts'))
    categories = Category.query.all()
    return render_template('product/create.html',categories=categories)

# Update record
@app.route('/editproduct/<int:id>', methods=['GET', 'POST'])
@login_required
def editproduct(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.commission = request.form['commission']
        product.category_id = request.form['category_id']
        product.sub_category_id = request.form['sub_category_id']
        product.sub_sub_category_id = request.form['sub_sub_category_id']
        product.cost = request.form['cost']
        product.image = request.form['image']
        product.status = request.form['status']
        product.highlights = request.form['highlights']
        product.description = request.form['description']
        db.session.commit()
        return redirect(url_for('indexproducts'))
    categories = Category.query.all()
    return render_template('product/edit.html', product=product,categories=categories)

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
        parent_category_id = request.form['parent_category_id']
        type = request.form['type']
        category = Category(name=name,title=name,parent_category_id=parent_category_id,type=type)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('indexcategories'))
    categories = Category.query.all()
    return render_template('category/create.html',categories=categories)

# Update record
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.type = request.form['type']
        
        category.parent_category_id = request.form['parent_category_id']
        db.session.commit()
        return redirect(url_for('indexcategories'))
    categories = Category.query.all()
    return render_template('category/edit.html', category=category,categories=categories)

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
        status = request.form['status']
        payment = Payment(total=total,user_id=user_id,status=status)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('indexpayments'))
    users = User.query.all()
    return render_template('payment/create.html',users=users)

# Update record
@app.route('/editpayment/<int:id>', methods=['GET', 'POST'])
@login_required
def editpayment(id):
    payment = Payment.query.get(id)
    if request.method == 'POST':
        payment.total = request.form['total']
        payment.user_id = request.form['user_id']
        payment.status = request.form['status']
        db.session.commit()
        return redirect(url_for('indexpayments'))
    users = User.query.all()
    return render_template('payment/edit.html', payment=payment,users=users)



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

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     data = Category.query.all()
    
#     categoryString = ""
#     for category in data:
#          #formatted_price = locale.format_string("%d", product.price, grouping=True)
#         #  formatted_price = "{:,}".format(int(product.price))
#          categoryString=categoryString+str(category.name)+" "+"<br/>"
#     return render_template('index.html', categories=categoryString,productlinkcount=productlinkcount)

# # @app.route('/orders')
# @login_required
# def orders():
#     orders = Order.query.all()
#     return "test"
#     return render_template('orders.html', orders=orders)

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