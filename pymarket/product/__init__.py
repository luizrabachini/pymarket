'''
Custom config to products
'''


def includeme(config):
	config.add_route('product_actions', '/product')
	
	config.add_route('product_add', '/product/new')
	config.add_route('product_remove', '/product/remove/{id}')
	
	config.add_route('product_list', '/product/list')
	config.add_route('product_edit', '/product/edit/{id}')

	config.add_route('product_select', '/product/select')
	config.add_route('product_cart_add', '/product/cart/add/{id}')
	config.add_route('product_cart_remove', '/product/cart/remove/{id}')
	config.add_route('product_cart_finalize', '/product/cart/finalize')
	config.add_route('product_cart_save', '/product/cart/save')
	config.add_route('product_cart_clear', '/product/cart/clear')

	config.scan('pymarket.product')