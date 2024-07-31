from django.shortcuts import render , get_object_or_404
from .cart import Cart
from store.models import Product
from django.contrib import messages
from django.http import JsonResponse



def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',{'cart_products':cart_products,"quantities":quantities , "totals":totals})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        name = request.POST.get('name')
        age = request.POST.get('age')

        print(f'Namse is : {name} and Age is : {age}')

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product , quantity=product_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty':cart_quantity})

        messages.success(request,('Adding to cart sucessfully........'))

        return response

    return render(request, 'cart_add.html')



#-----------from github------------

# from django.shortcuts import render, get_object_or_404
# from .cart import Cart
# from store.models import Product
# from django.http import JsonResponse
# from django.contrib import messages

# def cart_summary(request):
# 	# Get the cart
# 	cart = Cart(request)
# 	cart_products = cart.get_prods
# 	quantities = cart.get_quants
# 	totals = cart.cart_total()
# 	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})




# def cart_add(request):
# 	# Get the cart
# 	cart = Cart(request)
# 	# test for POST
# 	if request.POST.get('action') == 'post':
# 		# Get stuff
# 		product_id = int(request.POST.get('product_id'))
# 		product_qty = int(request.POST.get('product_qty'))

# 		# lookup product in DB
# 		product = get_object_or_404(Product, id=product_id)
		
# 		# Save to session
# 		cart.add(product=product, quantity=product_qty)

# 		# Get Cart Quantity
# 		cart_quantity = cart.__len__()

# 		# Return resonse
# 		# response = JsonResponse({'Product Name: ': product.name})
# 		response = JsonResponse({'qty': cart_quantity})
# 		messages.success(request, ("Product Added To Cart..."))
# 		return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request,('Items deleted from  cart sucessfully........'))

        return response



def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})

    
        messages.success(request,('Update to cart sucessfully........'))


        return response
    
    


    return render(request, 'cart_update.html')