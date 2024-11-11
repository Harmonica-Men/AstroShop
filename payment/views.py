from django.shortcuts import render, redirect
from shopcart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem, PaymentOfPayPal
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

import uuid # unique user id for duplictate orders

from .forms import PaymentForm  # Ensure you are importing the form


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

            print("Your Info Has Been Updated!!")
            return redirect('products')  # Redirect after saving

        # If forms are not valid, return the same page with the forms
        return render(request, "payment/update_payment_paypal.html", {'pay_form': pay_form, 'payment_form': payment_form})

    else:
        # If the user is not logged in, redirect to the homepage with a warning
        messages.warning(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')




def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('products')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def process_order(request):
	if request.POST:
		print('test')
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")

			print("delete old_cart")


			print("Order Placed!")
			return redirect('home')

			

		else:
			# not logged in
			
			print('process order not logged in ')
			
			
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('home')


	else:
		messages.success(request, "Access Denied")
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

	for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

	return render(request, "payment/payment_success.html", {})

	


def payment_failed(request):
	return render(request, "payment/payment_failed.html", {})