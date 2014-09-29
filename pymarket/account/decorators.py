'''
account / decorator
'''

## Pyramid Core
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound


def login_required(func):
	'''
	Redirect user to login page if not authenticated
	'''

	def decorator(request, *args, **kwargs):
		if authenticated_userid(request) is None:
			loc = request.route_url('signin', _query=(('next', request.path),))
			return HTTPFound(location=loc)

		return func(request, *args, **kwargs)			

	return decorator