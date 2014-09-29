'''
Main configuration
'''

from pyramid.config import Configurator
## Auth
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
## Database (MongoDB)
from urlparse import urlparse
from gridfs import GridFS
import pymongo
## Security
from .security import userfinder
## Extra
from pymarket.account.utils import get_user


def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings,
		session_factory=SignedCookieSessionFactory('********'))

	config.add_static_view('static', 'static', cache_max_age=3600)

	# Security policies
	authn_policy = AuthTktAuthenticationPolicy(
		settings['pymarket.secret'], callback=userfinder,
		hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)

	## Apps
	config.include('pymarket.account')
	config.include('pymarket.master')
	config.include('pymarket.product')
	config.scan()

	## Custom conf
	config.add_request_method(get_user, 'user', reify=True)

	## Database configuration
	db_url = urlparse(settings['mongo_uri'])
	config.registry.db = pymongo.Connection(
		host=db_url.hostname,
		port=db_url.port,
	)

	def add_db(request):
		db = config.registry.db[db_url.path[1:]]
		if db_url.username and db_url.password:
			db.authenticate(db_url.username, db_url.password)
		return db

	def add_fs(request):
		return GridFS(request.db)

	config.add_request_method(add_db, 'db', reify=True)
	config.add_request_method(add_fs, 'fs', reify=True)

	return config.make_wsgi_app()
