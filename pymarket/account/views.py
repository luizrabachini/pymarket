'''
account / views
'''

## Pyramid Core
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
## Database
from bson.objectid import ObjectId
## Forms
from pymarket.account.forms import SignupForm


@view_config(route_name='signup')
@view_config(route_name='settings')
def signup(request):
	'''
	Signup of new users
	'''

	user = None
	user_id = request.matchdict.get('id')
	user_id_obj = None
	is_update = False

	messages = []

	if user_id:
		is_update = True
		user_id_obj = ObjectId(user_id)
		user = request.db['users'].find_one({'_id':user_id_obj})

	form = SignupForm(request.POST, data=user)

	if request.method == 'POST' and form.validate():
		user = request.db['users'].find_one({'email':form.data['email']})
		if not user or user['_id'] == user_id_obj:
			if user_id:
				request.db['users'].update({'_id':user_id_obj}, {"$set":form.data}, upsert=False)
			else:
				request.db['users'].insert(form.data)
			headers = remember(request, form.data['email'])
			loc = request.route_url('home')
			return HTTPFound(location=loc, headers=headers)
		else:
			messages.append('E-mail already in use. Please, select another.')

	ret = {
		'form':form,
		'messages':messages,
		'is_update':is_update,
		}


	return render_to_response('templates/account/signup.jinja2', ret, request=request)


@view_config(route_name='signin')
def signin(request):
	'''
	Check and adds user authorization
	'''

	messages = []

	if request.POST:
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		user = request.db['users'].find_one({'email':email, 'password':password})

		if user:
			headers = remember(request, email)
			loc = request.params.get('next') or request.route_url('home')
			return HTTPFound(location=loc, headers=headers)
		else:
			messages.append('E-mail or password incorrects.')

	ret = dict(
		messages=messages,
		logged_in = request.authenticated_userid
		)

	return render_to_response('templates/account/signin.jinja2', ret, request=request)


@view_config(route_name='signout')
def signout(request):
	'''
	Removes user authorization
	'''

	headers = forget(request)

	return HTTPFound(location=request.route_url('site'), headers=headers)