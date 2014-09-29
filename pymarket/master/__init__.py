'''
Custom config to master
'''


def includeme(config):
	config.add_route('site', '/')
	config.add_route('home', '/home')
	
	config.scan('pymarket.master')