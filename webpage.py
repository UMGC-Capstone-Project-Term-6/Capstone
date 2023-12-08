"""
Python Web Page Code

Creates a unique web page using the flask framework1
"""
import csv, html
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm, PasswordUpdateForm

# Starting Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'iamamonkey123456789'

now = datetime.now()

# Setting up data
location_routes = {"California": "california_jobs.html", "WashingtonDC": "washingtondc_jobs.html",
                   "Maryland": "maryland_jobs.html",
                   "Utah": "utah_jobs.html", "Virginia": "virginia_jobs.html", "Washington": "washington_jobs.html"}

job_routes = {"SoftwareEngineer": "softwareEngineer.html", "DataAnalyst": "dataAnalyst.html", "CyberSecurityEngineer":
    "cyberSecurityEngineer.html", "GameDeveloper": "gameDeveloper.html", "SystemsEngineer": "systemsEngineer.html"}

jobs_list = {"SoftwareEngineer": "_swe.html", "CyberSecurityEngineer": "_cyber.html", "DataAnalyst": "_data.html",
             "GameDeveloper": "_game.html", "SystemsEngineer": "_sys.html"}


@app.route('/', methods=['GET', 'POST'])
@app.route("/home")
@login_required
def home():
    if request.method == 'POST':
        location = request.form['area']
        job = request.form['job']

        location_selection = location_routes.get(location)
        job_selection = job_routes.get(job)
        redirect_url = ""
        if location == "NoSelection" and job != "NoSelection":
            redirect_url = url_for('redirect_to_only_job', job_area=job_selection)
            return redirect(redirect_url)
        elif job == "NoSelection" and location != "NoSelection":
            redirect_url = url_for('redirect_to_only_location', location_area=location_selection)
            return redirect(redirect_url)
        elif location_selection != "NoSelection" and job_selection != "NoSelection":
            curr_job = job
            job_selection = location.lower() + jobs_list.get(curr_job, "")
            redirect_url = url_for('redirect_to_full_page', job=job_selection)
            return redirect(redirect_url)

    return render_template('home.html')

def create_html_table(file):
    # Manual adjustment whenever washington dc is found since no csv exists.
    file = file.replace("washingtondc", "maryland")

    csv_file_path = "jobs_data/" + file[:-5] + ".csv"
    csv_data = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            csv_data.append(row)

    html_table = '<table border="1" style="table-layout: fixed; width: 100%">\n'

    html_table += '<tr>'
    for header_cell in header:
        html_table += f'<th style="word-wrap: break-word;">{html.escape(header_cell)}</th>'
    html_table += '</tr>\n'

    for row in csv_data:
        html_table += '<tr>'
        for cell in row:

            if cell.startswith("http://") or cell.startswith("https://"):
                html_table += f'<td style="word-wrap: break-word;"><a href="{cell}" target="_blank">{html.escape(cell)}</a></td>'
            else:
                html_table += f'<td style="word-wrap: break-word;">{html.escape(cell)}</td>'
        html_table += '</tr>\n'

    html_table += '</table>'
    return html_table

def find_html_page(job):

    state = ""
    state_flag = False
    job_type = ""
    job_flag = False
    for character in job:
        if(character != "_" and state_flag == False):
            state += character
        elif (character == "_" or state_flag == True):
            state_flag = True
            job_type += character

    html_page = state + job_type
    return html_page

@app.route('/job/<job>')
def redirect_to_full_page(job):
    html_page = find_html_page(job)
    table = create_html_table(html_page)
    return render_template(html_page, table=table)


@app.route('/location/<location_area>')
def redirect_to_only_location(location_area):
    return render_template(location_area)


@app.route('/job_area/<job_area>')
def redirect_to_only_job(job_area):
    return render_template(job_area)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Routes to the webpage using Flask framework. Page for registration of
    a user. Checks if a users username or email exists in the database (.txt).
    Writes the new information to a new line in the database (.txt) to create
    a user.

    Parameters
    ----------
    N/A

    Returns
    -------
    render_template
        Returns the 'home.html' webpage

    """
    form = RegistrationForm()

    if form.validate_on_submit():

        # Reading user_data.txt for existing user
        with open("user_data.txt", "r", encoding="utf-8") as file:
            existing_users = file.readlines()

            # Checking all users
            for user in existing_users:
                user_data = user.strip().split(',')
                username, email, *_ = user_data

                # If the username or the email exist, give message and not allow registration
                if form.username.data == username or form.email.data == email:
                    flash("Username or Email Exists!")
                    return redirect(url_for('register'))

        # Writing to user_data.txt database new user information
        with open("user_data.txt", "a", encoding="utf-8") as file:
            file.write(f"{form.username.data},{form.email.data},"
                       f"{form.password.data}, 'No Secret'\n")
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Routes to the webpage using Flask framework. Page for logging in to
    the website. Checks if the email and password match what is in the
    database (.txt). GIves a message for success and unsuccessful attempts.
    Logs any failed attempts if it is an existing user.


    Parameters
    ----------
    N/A

    Returns
    -------
    render_template
        Returns the 'login.html' webpage or redirects to home

    """
    form = LoginForm()

    is_failed_attempt = False

    failed_email = ''

    if form.validate_on_submit():

        # Opening the file to read
        with open("user_data.txt", "r", encoding="utf-8") as file:
            users = file.readlines()

            # Going through each user
            for user in users:
                user_data = user.strip().split(',')

                # Adding check if the length of the line is less than 4 items
                if len(user_data) != 4:
                    continue
                username, email, pwd, *_ = user_data

                # Checking if email and password match
                if form.email.data == email and form.password.data == pwd:
                    user = User(username, email, pwd)
                    login_user(user)
                    flash('You have been logged in!', 'success')
                    return redirect(url_for('home'))

                # If email matches but not password, we log this failed attempt
                if form.email.data == email and form.password.data != pwd:
                    is_failed_attempt = True
                    failed_email = email

            # If nothing is returned, an error message appears
            flash('Login Unsuccessful. Please check username and password', 'danger')

        # If a failed attempt of an email, we log the attempt
        if is_failed_attempt:
            ipaddress = request.remote_addr
            failed_date_time = now

            # Opening the logger.txt file to write the IP Address, date/time, and the email
            with open("logger.txt", "a", encoding="utf-8") as file:
                file.write(f"IP: {ipaddress}, Date & Time: {failed_date_time}, "
                           f"Email: {failed_email}\n")

    return render_template('login.html', title='Login', form=form)


@app.route("/password_update", methods=['GET', 'POST'])
@login_required
def password_update():
    """
    Routes to the password update webpage using Flask framework. Allows a user
    to update their password and associated secret if they provide a valid
    existing email and password combination. The function checks the existing
    records in the database (user_data.txt) and updates the password and secret
    if a match is found.

    Parameters
    ----------
    N/A

    Returns
    -------
    render_template
        Returns the 'password_update.html' webpage after an attempt. Redirects
        to the home page if the update is successful.

    """
    form = PasswordUpdateForm()

    if form.validate_on_submit():

        # Reading the users
        with open("user_data.txt", "r", encoding="utf-8") as file:
            users = file.readlines()

        updated = False

        # Iterating through the users, getting data
        for i, user in enumerate(users):
            username, email, pwd, *_ = user.strip().split(',')

            # If the inputted email and password exist, then replace the users data
            if form.email.data == email and form.password.data == pwd:
                users[i] = f"{username},{email},{form.new_password.data}," \
                           f"{form.password_secret.data}\n"
                updated = True
                break

        # If the update was successful, write the new information, give success message
        if updated:
            with open("user_data.txt", "w", encoding="utf-8") as file:
                file.writelines(users)
                flash('Password and secret have been updated!', 'success')
                return redirect(url_for('home'))
        else:
            flash('Update unsuccessful. Please check your old password.', 'danger')

    return render_template('password_update.html', title='Password Update', form=form)


@app.route("/logout")
@login_required
def logout():
    """
    Routes to the webpage using Flask framework. Logs out the current
    user in the website. Disallows access to @login_required routes.

    Parameters
    ----------
    N/A

    Returns
    -------
    render_template
        Returns the 'home.html' webpage

    """
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))


# Sets up the login manger to use for logging in.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    """
    Creates a User object to be used when creating a new user.

    Parameters
    ----------


    """

    def __init__(self, username, email, password):
        """
        Routes to the webpage using Flask framework. Will always route
        to root folder.

        Parameters
        ----------
        username

        email

        password

        """
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        """
        Gets the ID as the users email.

        Parameters
        ----------
        self

        Returns
        -------
        email
            user's email

        """
        return self.email

    @login_manager.user_loader
    def load_user(self):
        """
        Gets the current users information and loads it as a main
        account.

        Parameters
        ----------
        N/A

        Returns
        -------
        User
            Object of a user
        """
        with open("user_data.txt", "r", encoding="utf-8") as file:
            users = file.readlines()
            for user in users:
                username, email, pwd = user.strip().split(',')[:3]
                if email == self:
                    return User(username, email, pwd)
        return None


if __name__ == "__main__":
    app.run(debug=True)
