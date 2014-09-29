'''
pymarket / security
'''

def userfinder(userid, request):
	user = request.db['users'].find_one({'email':userid})
	if user:
		return user['email']