from django.urls import path
from . import views
from .views import update_product, add_product

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('product/delete/confirm/<int:pk>/', views.delete_product_confirmation, name='delete_product_confirmation'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('product/add/', add_product, name='add_product'),
    path('products', views.all_products, name='products')
]