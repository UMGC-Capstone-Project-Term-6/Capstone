"""
Developer: Jonathan Quinn
Lab 8: Security and Cipher Tools
Program that is used to generate a website through the use of python Flask.
Once the user is at the website, they are required to register and login.
The user is then able to navigate to more pages.
The website is for cybersecurity awareness which informs readers of the different topics
in reference to cybersecurity, and allows users to ask questions as well as see
questions that have already been asked. An Update Password tab has also been added.
Users can now update their passwords and must have the proper password complexity.
"""

import datetime
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'MeElAb09!@08@!'
COMMON_PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), 'CommonPasswords.txt')

# Initialize session
app.config['Session_TYPE'] = 'filesystem'
app.config['Session_PERMANENT'] = False
app.config['Session_ISE_SIGNER'] = True
app.config['Session_FILE_THRESHOLD'] = 100
app.config['Session_FILE_DIR'] = '/tmp/flask_session'
app.config['Session_FILE_MODE'] = 384
app.secret_key = 'MeElAb09!@08@!'
sess = Session()

# Method to develop a table
def create_table(database_names: str):
    """If database table has not been created, this function will create one"""
    conn = sqlite3.connect(database_names)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                    (name Text, email Text, questions Text)''')
    conn.commit()
    conn.close()


# Method to call create_table
create_table('databases_files.db')


# Route for Home page
@app.route('/homepage')
def homepage():
    """Home page that allows users to navigate to other sites."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('homepage.html', title='', current_time=current_time)


# Log file path
LOG_FILE = 'login.log'


# If log file does not exist, create
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='uft-8') as f:
        f.write('Date,IP Address\n')


# Function for failed login
def log_login_attempt():
    """This function logs failed login attempts"""
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr
    with open(LOG_FILE, 'w', encoding='utf-8') as f_log:
        f_log.write(f'{date},{ip_address}\n')


# Check for common passwords
def check_common_password(password):
    """Check the list of passwords that are commonly used"""
    with open(COMMON_PASSWORDS_FILE, 'r', encoding='utf-8') as f_log:
        common_passwords = [line.strip() for line in f_log.readlines()]
    if password in common_passwords:
        return True
    return False


# Route and method for login
@app.route('/', methods=['GET', 'POST'])
def login():
    """Sign user in"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect("databases_files.db")

        cur = con.cursor()
        cur.execute("select * from users where username=? and password=?", (username, password))
        session['name'] = username
        if not cur.fetchone():
            log_login_attempt()
            flash("Invalid username or password", "Invalid")
            return render_template('login.html')
        if check_common_password(password):
            flash("Password is common use another", "Invalid")
            return render_template('login.html')

        return render_template('homepage.html', title='',
                               current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return render_template('login.html')


# Route and function for register
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Users are given the opportunity to register if they do not have an account"""
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            con = sqlite3.connect("databases_files.db")
            cur = con.cursor()
            cur.execute("insert into users(username, password, email) values (?, ?, ?)",
                        (username, password, email))
            con.commit()
            session['name'] = username
        except sqlite3.Error:
            flash("Error in inserting", "invalid")
        finally:
            con.close()
        return render_template('homepage.html', title='',
                               current_time=datetime.datetime.now().strftime
                               ('%Y-%m-%d %H:%M:%S'))
    return render_template('register.html')


# Route and method for email and phone number
@app.route('/contact')
def contact():
    """If the user clicks on the "Contact Us" link,"
    they will see the contact information."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('contact.html', title='Contact Us', current_time=current_time)


# Route as well as method to ask a question
@app.route('/questions')
def questions():
    """If the user clicks on the "Ask a Question" link,"
        they have an opportunity to ask a question."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('questions.html', title='Questions', current_time=current_time)


# Method to develop another table
def create_table1(database_names: str):
    """If database table has not been created, this function will create one"""
    conn = sqlite3.connect(database_names)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (username Text, password Text, email Text)''')

    conn.commit()
    conn.close()


# Method to call creates_table
create_table1('databases_files.db')


# Route as well as method to see questions that have already been asked
@app.route('/asked', methods=['GET', 'POST'])
def asked():
    """User has the opportunity to see what questions have already been asked"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        question = request.form['questions']

        conn = sqlite3.connect('databases_files.db')
        cursor = conn.cursor()
        data = (name, email, question)
        cursor.execute("INSERT INTO questions (name, email, questions) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()

        return redirect(url_for('homepage'))

    conn = sqlite3.connect('databases_files.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    fetched_asked = cursor.fetchall()
    conn.close()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template('asked.html', title='Questions Asked',
                           questions=fetched_asked, current_time=current_time)


# Route as well as method for images
@app.route('/images')
def images():
    """method for images which has been created in html."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    return render_template("images.html")


# Route as well as method for table
@app.route('/table')
def table():
    """method for table which has been created in html."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    return render_template("table.html")


# Route as well as method for logout
@app.route('/logout')
def logout():
    """method for logout  which has been created in html."""
    session.clear()
    return render_template("login.html")


# Route as well as function to update password
@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    """method to update password."""
    if session.get('name') is None:
        return redirect(url_for("login"))
    if request.method == 'POST':
        old_password = request.form['current_password']
        password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        con = sqlite3.connect("databases_files.db")
        cur = con.cursor()
        cur.execute("select * from users where username=?", (session['name'],))
        user = cur.fetchone()
        if user and user[1] == old_password:
            if password == confirm_password:
                cur.execute("update users set password = ? where username=?",
                            (password, session['name'],))
                con.commit()
                flash("Password updated successfully", "success")
            return render_template('homepage.html')
        flash("that is incorrect", "Invalid")
    return render_template("update_password.html", title='Update Password')
