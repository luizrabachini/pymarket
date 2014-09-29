'''
account / forms
'''

## Forms Core
from wtforms import Form, PasswordField, TextField, validators


class SignupForm(Form):
	'''
	Form to signup
	'''

	first_name = TextField('First Name', [
		validators.Length(min=4, max=25),
		validators.Required(message='First Name is required')])
	last_name = TextField('Last Name', [
		validators.Length(min=4, max=25),
		validators.Required(message='Last Name is required')])
	email = TextField('Email', [
		validators.Length(min=6, max=25),
		validators.Required(message='First Name is required'),
		validators.Email(message='Your email is invalid')])
	password = PasswordField('Password', [
		validators.Length(min=6),
		validators.Required(message='Password is required')])
	password_conf = PasswordField('Confirm password', [
		validators.Length(min=4),
		validators.EqualTo('password', message='Passwords must match')])