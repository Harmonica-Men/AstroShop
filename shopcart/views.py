from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def shopcart_summary(request):	
	return render(request, "shopcart_summary.html", {})
	
def shopcart_add(request):
	pass

def shopcart_delete(request):
    pass

def shopcart_update(request):
	pass
