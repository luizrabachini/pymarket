'''
product / utils
'''


def update_amount_price(request):
	'''
	Update amount to pay
	'''

	current_cart = request.session.get('current_cart')
	amount = 0

	for product_id_obj in current_cart:
		product = request.db['products'].find_one({'_id':product_id_obj})
		amount += product['price']

	request.session['amount'] = amount