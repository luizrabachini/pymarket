'''
product / forms
'''

## Forms Core
from wtforms import Form, TextField, FloatField, validators
from wtforms.widgets import TextArea


class EditProductForm(Form):
	'''
	Form to edit product
	'''

	name = TextField('Name', [
		validators.Required(message='Name is required')])
	description = TextField('Description', [
		validators.Required(message='Description is required')],
		widget=TextArea())
	price = FloatField('Price', [
		validators.Required(message='Price is required')])