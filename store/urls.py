from django.urls import path
from . import views

from .views import update_product, add_product, SubscribeView, CheckEmailView, confirm_subscription

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),

    path('update_ship_profile/', views.update_ship_profile, name='update_ship_profile'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),

    path('update_user_and_shipping_profile/', views.update_user_and_shipping_profile, name='update_user_and_shipping_profile'),
    # path('update_user_profile/', views.update_user_profile, name='update_user_profile'),

    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),

    path('search/', views.search, name='search'),
    path('product/delete/confirm/<int:pk>/', views.delete_product_confirmation, name='delete_product_confirmation'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('product/add/', add_product, name='add_product'),
    path('products/', views.all_products, name='products'),
     # Subscribe to a newsletter or service
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    # Check email view
    path('check-email/', views.CheckEmailView.as_view(), name='check-email'),

    path('shopper/confirm/', views.confirm_subscription, name='confirm_subscription'),



    path('test_email/', views.send_mail_page, name='test_email')

   
]