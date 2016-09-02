from flask import Flask, render_template,request,url_for
from flask_wtf import Form
from wtforms.fields import TextField ,TextAreaField, SubmitField, PasswordField 
from wtforms import validators , ValidationError
from wtforms.validators import Required
import datetime 
import MySQLdb


class RegistrationForm(Form):
    name = TextField('name', [validators.Length(min=4, max=20)])
    email = TextField('email', [validators.Length(min=10, max=50)])
    password = PasswordField('password', [validators.Length(min=6, max=50)])
    submit = SubmitField('Signup')
            