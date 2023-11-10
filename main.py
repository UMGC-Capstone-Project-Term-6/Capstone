"""
# Alexander Phillips
# Building Secure Python Applications
# SDEV 300 6382 Building Secure Python
# lab 8
# March 7, 2023
#   Description: This is just a python flask application, building a website
                 nothing to fancy just lots of editing with the incoming projects
"""
import fileinput
# imports
import webbrowser
from datetime import datetime
from threading import Timer
from flask import Flask, request, render_template
from passlib.hash import sha256_crypt

SPECIAL_CHARACTERS = {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')'}

rotation = ['Hammer of Wrath', 'Crusader Strike', 'Judgement of Wisdom',
            'Divine Storm', 'Consecration', 'Exorcism']
gear = {'Helm': ['Tier', 'Mimirons Flight Goggles', 'Warhelm of the Champion'],
        'Shoulders': ['Shoulderpads of the Intruder', 'Tier'],
        'Back ': ['Drape of Icy Intent', 'Drape of the Faceless General'],
        'Chest': ['Tier', 'Embrace of the Gladiator'],
        'Wrist': ['Armbands of Bedlam', 'Solar Bindings', 'Bitter Cold Armguards'],
        'Hands': ['Tier', 'Gloves of the Steady Hand'],
        'Waist': ['Soul-Devouring Cinch', 'Belt of Colossal Rage',
                  'Belt of the Titans'],
        'Legs ': ['Tier', 'Plated Leggings of Ruination'],
        'Feet': ['Sabatons of Lifeless Night', 'Tempered Mercury Greaves',
                 'Battlelords Plate Boots'],
        'Jewelry ': ['Pendulum of Infinity', 'Strength of the Heavens',
                     'Insurmountable Fervor'],
        'Rings': ['Branns Signet Ring', 'Seal of the Betrayed King',
                  'Branns Sealing Ring', 'Loop of the Agile'],
        'Trinkets': ['Darkmoon Card: Greatness', 'Comets Trail',
                     'Dark Matter', 'Wrathstone'],
        'Weapons': ['Voldrethar, Dark Blade of Oblivion', 'Aesirs Edge',
                    'Hammer of Crushing Whispers', 'Earthshaper'],
        'Libram': ['Furious Gladiators Libram of Fortitude'],
        }

logged_user = []

app = Flask(__name__)


@app.route('/')
def home():
    """ Home render for the website"""
    return render_template('home.html', gear=gear)


@app.route('/about/')
def about():
    """ about render for the website"""
    return render_template('about.html', datetime=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


@app.route('/dps_rotation/')
def dps_rotation():
    """ dps_rotation render for the website"""
    return render_template('DpsRotation.html', rotation=rotation)


@app.route('/mounts/')
def mounts():
    """ dps_rotation render for the website"""
    return render_template('Mounts.html')


@app.route('/update/', methods=['GET', 'POST'])
def update_info():
    """ update render for the website"""
    if request.method == 'GET':  # If the request is GET we return the
        # sign
        if len(logged_user) > 0:
            return render_template('Update.html', user=logged_user[0])
        return render_template('UpdateNotLoggedIn.html')
    item = request.form.get('item')
    if read_commons(item):
        return render_template('Update.html', user=logged_user[0],
                               info='Please remove common phrases from password')
    if check_item(item):
        hash_pass = sha256_crypt.hash(item)
        save_update(logged_user[0], hash_pass)
        return render_template('Update.html', user=logged_user[0], info="Success Edit!")

    return render_template('Update.html', user=logged_user[0],
                           info='Password not complex enough ')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    """ registration_rotation render for the website"""
    if request.method == 'GET':  # If the request is GET we return the
        # sign up page and forms
        return render_template('Register.html')
    item = request.form.get('item')
    username = request.form.get('username')
    player_class = request.form.get('wowclass')
    if read_commons(item):
        return render_template("Register.html", info='Please remove common phrases from password')
    if is_good_inputs(item, username):
        hash_pass = sha256_crypt.hash(item)
        results = save(username, player_class, hash_pass)
        if results:
            return render_template("Register.html", info='Account has been created.')
    else:
        return render_template("Register.html", info='Password not complex enough ')

    return render_template("Register.html", info='That Username already exists')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ login_rotation render for the website"""
    if request.method == 'GET':  # If the request is GET we return the
        # sign up page and forms
        return render_template('Login.html')
    item = request.form.get('item')
    username = request.form.get('username')
    if is_good_inputs(item, username):
        good_or_not = login_file_read(username, item)
        if good_or_not:
            if len(logged_user) > 0:
                logged_user.pop()
            logged_user.append(username)
            return render_template("Successful.html", logged_name=username)
    logger()
    return render_template("Login.html", info='Invalid Password or Username')


def login_file_read(username, code):
    """ login read file"""
    found_line = read_file(username)
    if found_line is None:
        return False
    if found_line[0] == username:
        if sha256_crypt.verify(code, found_line[2]):
            return True
    return False


def read_file(name, filepath='static/data/database.txt'):
    """Method: read_cvs_file_data
        variables: name, header rows
        returns the split of the line if it matches the name
        """
    try:
        with open(filepath, 'r', encoding='UTF-8') as file:
            for line in file:
                split = line.split(' ')
                if split[0] == name:
                    return split
        return None
    except IOError:
        return None


def logger(filepath='static/data/Logger.txt'):
    """ Save the userinfo"""
    with open(filepath, "a+", encoding='UTF-8') as file:
        file.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                   + " " + request.environ['REMOTE_ADDR'] + " \n")


def save(name, player_class, code, filepath='static/data/database.txt'):
    """ Save the userinfo"""
    found_line = read_file(name)
    if found_line is None:
        with open(filepath, "a+", encoding='UTF-8') as file:
            file.write(name + " " + player_class + " " + code + " \n")
            return True
    return False


def save_update(name, data, filepath='static/data/database.txt'):
    """ Save the userinfo"""
    with fileinput.FileInput(filepath,
                             inplace=True, backup='', encoding='UTF-8') as file:
        for line in file:
            split = line.split(' ')
            if split[0] == name:
                print(split[0] + ' ' + split[1] + ' ' + data + ' ', end='\n')
            else:
                print(line, end='\n')


def is_good_inputs(item, username):
    """ check if the inputs were all good"""
    if username.isspace():
        return False
    if check_item(item) is False:
        return False
    return True


def open_browser_automatically():
    """ open_browser render for the website"""
    webbrowser.open_new("http://127.0.0.1:5000")


def check_item(potential_item):
    """ check password method,
        takes in a potential_password
        calls check_for_uppercase method
              check_for_lowercase method
              check_for_number method
              check_for_special method
        makes sure the password is good and secure
    """
    if potential_item.isspace():
        return False
    if len(potential_item) > 9:
        if check_for_uppercase(potential_item) and check_for_lowercase(potential_item):
            if check_for_number(potential_item) and check_for_special(potential_item):
                return True
    return False


def read_commons(potential_item, filepath='static/data/CommonPassword.txt'):
    """Method: read_cvs_file_data
        variables: name, header rows
        returns the split of the line if it matches the name
        """
    try:
        with open(filepath, 'r', encoding='UTF-8') as file:
            for line in file:
                line_item = line.strip()
                if line_item.upper() in potential_item.upper():
                    return True
        return False
    except IOError:
        return False


def check_for_uppercase(potential_item):
    """ check_for_uppercase method,
            takes in a potential_password
            makes sure the password has an upper case
    """
    for char in potential_item:
        if char.isupper():
            return True
    return False


def check_for_lowercase(potential_item):
    """ check_for_lowercase method,
            takes in a potential_password
            makes sure the password has a lower case
    """
    for char in potential_item:
        if char.islower():
            return True
    return False


def check_for_number(potential_item):
    """ check_for_number method,
            takes in a potential_password
            makes sure the password has a number
    """
    for char in potential_item:
        if char.isdigit():
            return True
    return False


def check_for_special(potential_item):
    """ check_for_special method,
            takes in a potential_password
            makes sure the password has a special character
    """
    for char in potential_item:
        if char in SPECIAL_CHARACTERS:
            return True
    return False


if __name__ == '__main__':
    # if 'fish'.upper() in 'FishPaste%2!23'.upper():

    Timer(1, open_browser_automatically).start()
    app.run()
