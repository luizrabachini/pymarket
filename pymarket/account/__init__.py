'''
Custom config to account
'''


def includeme(config):
	config.add_route('signin', '/signin')
	config.add_route('signout', '/signout')
	config.add_route('signup', '/signup')
	config.add_route('settings', '/settings/{id}')
	
	config.scan('pymarket.account')