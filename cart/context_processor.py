# from .cart import Cart


# def cart(request):
#     return{'cart': Cart(request)}



from .cart import Cart

# Create context processor so our cart can work on all pages of the site
def cart(request):
	# Return the default data from our Cart
	return {'cart': Cart(request)}