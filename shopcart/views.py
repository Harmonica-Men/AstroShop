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
		shopcart.add(product=product)

		# Return resonse
		response = JsonResponse({'Product Name: ': product.name})
		return response

def cart_delete(request):
	pass

def cart_update(request):
	pass