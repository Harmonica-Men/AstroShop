from django.shortcuts import render, redirect
from shopcart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem, PaymentOfPayPal
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
from django.utils import timezone
import datetime
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail



import uuid # unique user id for duplictate orders

from .forms import PaymentForm  # Ensure you are importing the form

from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def send_mail_update(request):
    user = request.user
    # Ensure user is authenticated
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': 'User not authenticated.'})

    # Prepare email context
    subject = 'order placed Success'
    message = render_to_string('confirmation_emails/confirmation_email_order.txt', {

    # message = render_to_string('confirmation_emails/confirmation_email_body.txt', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': user.pk,  # Include user ID if necessary
        'token': 'dummy_token',  # Replace with actual token logic if needed
    })

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    messages.success(request, ("Email send for Order"))

    return redirect('home')


    # messages.success(request, ("Email send order"))


def update_payment_paypal(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
		
        # Try to get existing PaymentOfPayPal record for the current user
        try:
            pay_user = PaymentOfPayPal.objects.get(user_paypal_id=request.user.id)  # Ensure user_paypal_id is set correctly
        except PaymentOfPayPal.DoesNotExist:
            pay_user = None  # No existing payment info for this user
        
        # Get original User Form for payment info
        pay_form = PaymentForm(request.POST or None, instance=current_user)
        
        # Get or create the payment form for the user’s PayPal info
        payment_form = PaymentForm(request.POST or None, instance=pay_user)
        
        if pay_form.is_valid() and payment_form.is_valid():
            # Save the user info form (this might be related to billing info)
            pay_form.save()

            if pay_user:  # If payment_user exists, update
                payment_form.save()  # Save the payment form (if updating existing record)
            else:
                # If no payment info exists, create a new record
                pay_user = payment_form.save(commit=False)
                pay_user.user = request.user
                # Ensure user_paypal_id is set before saving
                pay_user.user_paypal_id = request.user.id  # Assign the user ID as the PayPal ID
                pay_user.save()  # Save the new payment record

           
            return redirect('products')  # Redirect after saving

        # If forms are not valid, return the same page with the forms
        return render(request, "payment/update_payment_paypal.html", {'pay_form': pay_form, 'payment_form': payment_form})

    else:
        # If the user is not logged in, redirect to the homepage with a warning
        messages.warning(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            num = request.POST['num']
            # Set the order to unshipped and remove the date_shipped
            order = Order.objects.filter(id=num)
            order.update(shipped=False, date_shipped=None)
            messages.success(request, "Order marked as not shipped.")
            # Reload with updated data for unshipped orders
            return redirect('not_shipped_dash')
        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        return redirect('products')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            num = request.POST['num']
            # Set the order to shipped and add the current timestamp
            order = Order.objects.filter(id=num)
            order.update(shipped=True, date_shipped=timezone.now())
            messages.success(request, "Order marked as shipped.")
            # Reload with updated data for shipped orders
            return redirect('shipped_dash')
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        return redirect('products')

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                Order.objects.filter(id=pk).update(shipped=True, date_shipped=timezone.now())
            else:
                Order.objects.filter(id=pk).update(shipped=False)
            return redirect('not_shipped_dash')
        return render(request, 'payment/orders.html', {"order": order, "items": items})
    else:
        return redirect('home')

def billing_info(request):
    billing_form = PaymentForm()
    payment_form = PaymentForm()

    if request.POST:
        # Store shipping info in session
        my_shipping = {
            'shipping_full_name': request.POST.get('shipping_full_name'),
            'shipping_email': request.POST.get('shipping_email'),
            'shipping_address1': request.POST.get('shipping_address1'),
            'shipping_address2': request.POST.get('shipping_address2'),
            'shipping_city': request.POST.get('shipping_city'),
            'shipping_state': request.POST.get('shipping_state'),
            'shipping_zipcode': request.POST.get('shipping_zipcode'),
            'shipping_country': request.POST.get('shipping_country')
        }
        request.session['my_shipping'] = my_shipping

        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Set up PayPal payment dictionary
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Book Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),  # Generate invoice UUID
            'currency_code': 'EUR', 
            'notify_url': f'https://{host}{reverse("paypal-ipn")}',
            'return_url': f'https://{host}{reverse("payment_success")}',
            'cancel_return': f'https://{host}{reverse("payment_failed")}',
        }

        # Initialize PayPal form
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        if request.user.is_authenticated:
            user = request.user

            # Create Order
            create_order = Order(
                user=user,
                full_name=my_shipping['shipping_full_name'],
                email=my_shipping['shipping_email'],
                shipping_address="\n".join([my_shipping[key] for key in ['shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']]),
                amount_paid=totals,
                invoice=paypal_dict['invoice']  # Use invoice from PayPal dict
            )
            create_order.save()

            # Add Order Items
            for product in cart_products():
                quantity = quantities().get(str(product.id), 1)
                create_order_item = OrderItem(
                    order_id=create_order.pk,
                    product_id=product.id,
                    user=user,
                    quantity=quantity,
                    price=product.sale_price if product.is_sale else product.price
                )
                create_order_item.save()

            # Payment info
            try:
                pay_user = PaymentOfPayPal.objects.get(user_paypal_id=user.id)
                payment_form = PaymentForm(instance=pay_user)
            except PaymentOfPayPal.DoesNotExist:
                payment_form = PaymentForm()  # Empty form for new user

            return render(
                request,
                "payment/billing_info.html",
                {
                    "paypal_form": paypal_form,
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "invoice": paypal_dict['invoice'],  # Pass the generated invoice
                    "shipping_info": request.session['my_shipping'],
                    "billing_form": billing_form,
                    "payment_form": payment_form,
                }
            )
        else:
            return render(
                request,
                "payment/billing_info.html",
                {
                    "paypal_form": paypal_form,
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "invoice": paypal_dict['invoice'],  # Pass the generated invoice
                    "shipping_info": request.session['my_shipping'],
                    "billing_form": billing_form,
                    "payment_form": payment_form,
                }
            )


def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

	

def payment_success(request):

    # delete cookie session

    for key in list(request.session.keys()):
        if key == "session_key":
            # Delete the key
            del request.session[key]

    # the email order procedure

    user = request.user
    # Ensure user is authenticated
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': 'User not authenticated.'})

    # Prepare email context
    subject = 'order placed Success'
    message = render_to_string('confirmation_emails/confirmation_email_order.txt', {

    # message = render_to_string('confirmation_emails/confirmation_email_body.txt', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': user.pk,  # Include user ID if necessary
        'token': 'dummy_token',  # Replace with actual token logic if needed
    })

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    messages.success(request, ("Email send for Order"))

    return redirect('products')

    
    
    # return render(request, "payment/payment_success.html", {})

	


def payment_failed(request):
	return render(request, "payment/payment_failed.html", {})