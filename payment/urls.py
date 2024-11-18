from django.urls import path, include
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name="billing_info"),
    #path('process_order', views.process_order, name="process_order"),
    path('shipped_dash', views.shipped_dash, name="shipped_dash"),
    path('not_shipped_dash', views.not_shipped_dash, name="not_shipped_dash"),
    path('update_payment_paypal', views.update_payment_paypal, name='update_payment_paypal'),
    path('orders/', views.orders, name='orders'),
    path('orders/delete/<int:order_id>/', views.order_delete_confirmation, name='order_delete_confirmation'),
    path('paypal', include("paypal.standard.ipn.urls")),
]