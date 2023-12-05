"""
@name Kevin Pineda
@class SDEV 300 6980
@date 08/03/2023
Lab 8

Python Web Page Code

Sets up the forms to be used in the flask application
"""

import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    """
    A FlaskForm subclass for user registration.

    Attributes
    ----------
    username : StringField
        Input field for the username. Requires input with a minimum
        length of 2 and a maximum length of 20.

    email : StringField
        Input field for the user's email address.
        Requires a valid email format.

    password : PasswordField
        Input field for the user's password.

    confirm_password : PasswordField
        Input field to confirm the entered password.
        It must match the 'password' field.

    submit : SubmitField
        Button to submit the registration form.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    @staticmethod
    def validate_password(self, password):
        """
        Validates the password based on the following criteria:
        - At least 12 characters in length
        - At least 1 uppercase character
        - At least 1 lowercase character
        - At least 1 number
        - At least 1 special character.

        Parameters
        ----------
        password : Field
            The password field from the form.

        Raises
        ------
        ValidationError
            If the password does not meet the specified criteria.
        """
        rules = [
            len(password.data) >= 12,
            bool(re.search(r'[A-Z]', password.data)),
            bool(re.search(r'[a-z]', password.data)),
            bool(re.search(r'\d', password.data)),
            bool(re.search(r'\W', password.data))
        ]

        # Checking if the password contains any word from CommonPassword.txt
        with open("CommonPassword.txt", "r") as file:
            common_passwords = [pw.strip().lower() for pw in file.readlines()]
            user_password = password.data
            for common_pass in common_passwords:
                if common_pass in user_password:
                    raise ValidationError("This password contains a word that is too common. "
                                          "Please enter a different password.")

        if not all(rules):
            raise ValidationError("Password must be least 12 characters in length, and i"
                                  "nclude at least 1 uppercase character, 1 lowercase character, "
                                  "1 number and 1 special character.")


class LoginForm(FlaskForm):
    """
    A FlaskForm subclass for user login.

    Attributes
    ----------
    email : StringField
        Input field for the user's email address. Requires a valid email format.

    password : PasswordField
        Input field for the user's password.

    remember : BooleanField
        Checkbox to remember the user's session.

    submit : SubmitField
        Button to submit the login form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class PasswordUpdateForm(FlaskForm):
    """
    A FlaskForm subclass for updating user password.

    Attributes
    ----------
    email : StringField
        Input field for the user's email address. Requires a valid email format.

    password : PasswordField
        Input field for the user's current password.

    new_password : PasswordField
        Input field for the user's new password.

    confirm_password : PasswordField
        Input field to confirm the entered new password.
        It must match the 'new_password' field.

    password_secret : PasswordField
        Input field for an additional password secret.
        It's checked against common passwords.

    submit : SubmitField
        Button to submit the form to update the password.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Current Password', validators=[DataRequired()])

    new_password = PasswordField('New Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])

    password_secret = PasswordField('Add Password Secret', validators=[DataRequired()])

    submit = SubmitField('Update Password')

    @staticmethod
    def validate_new_password(self, new_password):
        """
        Validates the new password to ensure it meets complexity requirements.

        Parameters
        ----------
        new_password : PasswordField
            The new password entered by the user.
        """
        rules = [
            len(new_password.data) >= 12,
            bool(re.search(r'[A-Z]', new_password.data)),
            bool(re.search(r'[a-z]', new_password.data)),
            bool(re.search(r'\d', new_password.data)),
            bool(re.search(r'\W', new_password.data))
        ]

        if not all(rules):
            raise ValidationError("Password must be least 12 characters in length, "
                                  "and include at least 1 uppercase character,"
                                  " 1 lowercase character, 1 number and 1 special character.")

        # Checking if the password contains any word from CommonPassword.txt
        with open("CommonPassword.txt", "r") as file:
            common_passwords = [pw.strip().lower() for pw in file.readlines()]
            user_password = new_password.data
            for common_pass in common_passwords:
                if common_pass in user_password:
                    raise ValidationError("This password contains a word that is too common. "
                                          "Please enter a different password.")