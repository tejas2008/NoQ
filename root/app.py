from flask import Flask, render_template, request, redirect, url_for, session
import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'secret'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'

# Intialize MySQL
mysql = MySQL(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/customer/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        customer = cursor.fetchone()
        # If account exists in accounts table in out database
        if customer:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = customer['cus_id']
            session['username'] = customer['username']
            session['mobile'] = customer['mobileno']
            session['region'] = customer['region']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('cuslogin.html',msg=msg)


@app.route('/shop/login', methods=['GET', 'POST'])
def login1():
    # Check if "username" and "password" POST requests exist (user submitted form)
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM shop WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        shop = cursor.fetchone()
        # If account exists in accounts table in out database
        if shop:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = shop['shopid']
            session['username'] = shop['username']
            session['mobile'] = shop['mobile']
            session['region'] = shop['region']
            session['address'] = shop['address']
            session['shop_name'] = shop['shop_name']
            session['owner_name'] = shop['owner_name']
            # Redirect to home page
            return redirect(url_for('display'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('shoplogin.html',msg=msg)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')



@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/customer/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        region = request.form['region']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not mobile:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, %s,%s,%s)', (username, password, email,mobile,region))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('cuslogin.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('cusregister.html',msg=msg)


@app.route('/shop/register', methods=['GET', 'POST'])
def register1():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        ownername = request.form['ownername']
        shopname = request.form['shopname']
        mobile = request.form['mobile']
        address = request.form['address']
        region = request.form['region']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM shop WHERE username = %s', (username,))
        shop = cursor.fetchone()
        # If account exists show error and validation checks
        if shop:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not mobile or not address or not ownername or not shopname:
            print(1)
            msg = 'Please fill out the form!'
        else:
            print(3)
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO shop VALUES (NULL, %s, %s, %s,%s,%s,%s,%s)', (ownername,shopname,region,address,mobile,username, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('shoplogin.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        print(2)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('shopregister.html',msg=msg)

@app.route('/dashboard', methods=['GET', 'POST'])
def display():
    date1 = datetime.date.today() + datetime.timedelta(days=1)

    return render_template('shopdash.html',date1=date1,session=session)



if __name__ == '__main__':
    app.run(debug=True)

