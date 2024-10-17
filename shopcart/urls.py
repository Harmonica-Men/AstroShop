from django.urls import path
from . import views

urlpatterns = [
	path('', views.shopcart_summary, name="shopcart_summary"),
	path('add/', views.shopcart_add, name="shopcart_add"),
	# path('delete/', views.cart_delete, name="shopcart_delete"),
	# path('update/', views.cart_update, name="shopcart_update"),
]