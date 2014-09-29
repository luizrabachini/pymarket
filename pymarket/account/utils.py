'''
account / utils 
'''

from pyramid.security import unauthenticated_userid


def get_user(request):
	'''
	Return user information

	:Returns:
		User object from database.
		If user not found, None is returned.

	:Returns Type:
		User, if process success, or None, if process fail.
	'''

	userid = unauthenticated_userid(request)

	if userid is not None:
		return request.db['users'].find_one({'email':userid})

	return None