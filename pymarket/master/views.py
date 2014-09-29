'''
master / views
'''

## Pyrami Core
from pyramid.view import view_config
from pyramid.renderers import render_to_response
## Security
from pymarket.account.decorators import login_required


@view_config(route_name='site')
def site(request):
	'''
	Site
	'''

	return render_to_response('templates/master/site.jinja2',{}, request=request)


@view_config(route_name='home')
@login_required
def home(request):
	'''
	Home of user
	'''

	return render_to_response('templates/master/home.jinja2',{}, request=request)