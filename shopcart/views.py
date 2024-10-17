from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def shopcart_summary(request):
	return render(request, "shopcart_summary.html", {})


def shopcart_add(request):
	
	cart = Cart(request)
	
	if request.POST.get('action') == 'post':
	
		product_id = int(request.POST.get('product_id'))
		
	
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product)

		# Get Cart Quantity
		cart_quantity = cart.__len__()
		
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})

		return response

def shopcart_delete(request):
	pass

def shopcart_update(request):
	pass