from django.urls import path, include
from . import views

urlpatterns = [
    path('billing_info', views.billing_info, name="billing_info"),
    path('checkout', views.checkout, name='checkout'),
    path('no_orders_found/', views.no_orders_found, name='no_orders_found'),
    path('not_shipped_dash', views.not_shipped_dash, name="not_shipped_dash"),
    path('orders/', views.orders, name='orders'),
    path('orders/delete/<int:order_id>/', views.order_delete_confirmation, name='order_delete_confirmation'),
    path('orders_id/<int:pk>', views.orders_id, name='orders_id'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('shipped_dash', views.shipped_dash, name="shipped_dash"),
    path('update_payment_paypal/', views.update_payment_paypal, name='update_payment_paypal'),
    path('paypal', include("paypal.standard.ipn.urls")),
]
