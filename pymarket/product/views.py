'''
product / views
'''

## Pyramid Core
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
## Forms
from pymarket.product.forms import EditProductForm
## Database
from bson.objectid import ObjectId
## Utils
from pymarket.product.utils import update_amount_price
## Security
from pymarket.account.decorators import login_required
## Extra
from pymarket.account.utils import get_user
from datetime import datetime


## --------------------------------------------------
## Product Views
## --------------------------------------------------


@view_config(route_name='product_actions')
@login_required
def actions_product(request):
	'''
	Actions of products
	'''

	return render_to_response('templates/product/actions.jinja2', {}, request=request)


@view_config(route_name='product_add')
@view_config(route_name='product_edit')
@login_required
def edit_product(request):
	'''
	Edit product
	'''

	messages = []

	product = None
	product_id = request.matchdict.get('id')
	product_id_obj = None
	is_update = False

	if product_id:
		is_update = True
		product_id_obj = ObjectId(product_id)
		product = request.db['products'].find_one({'_id':product_id_obj})

	form = EditProductForm(request.POST, data=product)

	if request.method == 'POST' and form.validate():
		if product_id:
			request.db['products'].update({'_id':product_id_obj}, {"$set":form.data}, upsert=False)
			messages.append('Product updated!')
		else:
			request.db['products'].insert(form.data)
			messages.append('Product saved!')
			form = EditProductForm()

	ret = {
		'form':form,
		'messages':messages,
		'is_update':is_update,
		}

	return render_to_response('templates/product/form_product.jinja2', ret, request=request)


@view_config(route_name='product_list')
@login_required
def list_product(request):
	'''
	List products
	'''

	products = request.db['products'].find()

	ret = {
		'products':products,
		}

	return render_to_response('templates/product/list_product.jinja2', ret, request=request)


@view_config(route_name='product_remove')
@login_required
def remove_product(request):
	'''
	Remove product
	'''

	product_id = request.matchdict.get('id')
	product_id_obj = ObjectId(product_id)
	request.db['products'].remove({'_id':product_id_obj})

	# Update cart
	current_cart = request.session.get('current_cart')
	if current_cart:
		current_cart.remove(product_id_obj)
		update_amount_price(request)

	loc = request.route_url('product_list')
	return HTTPFound(location=loc)


## --------------------------------------------------
## Cart Views
## --------------------------------------------------


@view_config(route_name='product_select')
@login_required
def select_product(request):
	'''
	Show a list of products to select
	'''

	products = request.db['products'].find()

	user = get_user(request)
	carts = request.db['carts'].find({'user':user['_id']})

	ret = {
		'products':products,
		'carts':carts,
		}

	return render_to_response('templates/product/select_product.jinja2', ret, request=request)


@view_config(route_name='product_cart_add')
@login_required
def cart_add_product(request):
	'''
	Add product to cart
	'''

	product_id = request.matchdict.get('id')

	if product_id:
		current_cart = request.session.get('current_cart')
		product_id_obj = ObjectId(product_id)
		if not current_cart:
			request.session['current_cart'] = [product_id_obj]
		elif product_id_obj not in current_cart:
			current_cart.append(product_id_obj)

		update_amount_price(request)

		loc = request.route_url('product_select')
		return HTTPFound(location=loc)
	else:
		return NotFound()


@view_config(route_name='product_cart_remove')
@login_required
def cart_remove_product(request):
	'''
	Remove product from cart
	'''

	product_id = request.matchdict.get('id')

	if product_id:
		current_cart = request.session.get('current_cart')
		if current_cart:
			product_id_obj = ObjectId(product_id)
			current_cart.remove(product_id_obj)

		update_amount_price(request)

		loc = request.route_url('product_select')
		return HTTPFound(location=loc)
	else:
		return NotFound()


@view_config(route_name='product_cart_finalize')
@login_required
def cart_finalize_product(request):
	'''
	Finalize cart to show products
	'''

	current_cart = request.session.get('current_cart')
	if len(current_cart) > 0:
		products = request.db['products'].find({'_id': {'$in':current_cart}})
	else:
		products = None

	ret = {
		'products':products,
		}

	return render_to_response('templates/product/finalize_cart.jinja2', ret, request=request)


@view_config(route_name='product_cart_save')
@login_required
def cart_save_product(request):
	'''
	Save all products of cart
	'''

	current_cart = request.session.get('current_cart')
	if current_cart:
		user = get_user(request)
		products = []

		for product_id_obj in current_cart:
			product = request.db['products'].find_one({'_id':product_id_obj})
			products.append(product)
		
		request.db['carts'].insert(
			{'user':user['_id'],
			'products':products,
			'amount':request.session['amount'],
			'date_time':datetime.now()})

	del request.session['current_cart']

	loc = request.route_url('product_select')
	return HTTPFound(location=loc)


@view_config(route_name='product_cart_clear')
@login_required
def cart_clear_product(request):
	'''
	Remove all products from cart
	'''

	del request.session['current_cart']
	
	loc = request.route_url('product_select')
	return HTTPFound(location=loc)