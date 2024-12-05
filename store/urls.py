from django.urls import path
from . import views
from .views import (
    add_product, add_supplier, SubscribeView, delete_supplier,
    delete_product, general_conditions, disclaimer, payment,
    supplier_confirm_delete, supplier_detail, suppliers_list,
    update_product, update_user_and_shipping_profile,
    update_user_profile, update_password, logout_user, login_user,
    privacy, product, register_user, search, category,
    category_summary, CheckEmailView
)


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('check_email/', views.CheckEmailView.as_view(), name='check_email'),
    path('disclaimer/', disclaimer, name='disclaimer'),
    path('general_conditions/', views.general_conditions, name='general_conditions'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('payment/', payment, name='payment'),
    path('privacy/', privacy, name='privacy'),
    path('product/<int:pk>', views.product, name='product'),
    path('product/add/', add_product, name='add_product'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('product/delete/confirm/<int:pk>/', views.delete_product_confirmation, name='delete_product_confirmation'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('products/', views.all_products, name='products'),
    path('register/', views.register_user, name='register'),
    path('search/', views.search, name='search'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('suppliers/', suppliers_list, name='suppliers_list'),
    path('supplier/<int:supplier_id>/', supplier_detail, name='supplier_detail'),
    path('supplier/<int:supplier_id>/delete/', delete_supplier, name='supplier_delete'),
    path('supplier/<int:supplier_id>/confirm_delete/', supplier_confirm_delete, name='supplier_confirm_delete'),
    path('supplier/add/', add_supplier, name='add_supplier'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_user_and_shipping_profile/', views.update_user_and_shipping_profile, name='update_user_and_shipping_profile'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('update-ship-profile/', views.update_ship_profile, name='update_ship_profile'),
]
