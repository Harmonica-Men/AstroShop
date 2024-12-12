from django.shortcuts import render, get_object_or_404, redirect
from shopcart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem, PaymentOfPayPal
from .models import PaymentOfPayPal
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from store.models import Product, Profile
from django.utils import timezone
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .forms import PaymentForm
import datetime
import uuid



def update_payment_paypal(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

        try:
            pay_user = PaymentOfPayPal.objects.get(user_paypal_id=request.user.id)
        except PaymentOfPayPal.DoesNotExist:
            pay_user = None

        # Use PaymentForm
        payment_form = PaymentForm(request.POST or None, instance=pay_user)

        if payment_form.is_valid():
            pay_user = payment_form.save(commit=False)
            pay_user.user_paypal_id = request.user.id
            pay_user.save()
            return redirect('products')

        return render(request, "payment/update_payment_paypal.html", {'payment_form': payment_form})
    else:
        messages.warning(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def shipped_dash(request):
    """
    Displays a dashboard for superusers to view and manage shipped orders.
    Superusers can mark orders as unshipped,
    which resets the shipped status and date_shipped.
    """
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
    """
    Displays a dashboard for superusers,
    to view and manage orders not yet shipped.
    Superusers can mark orders as shipped,
    setting the current timestamp for the shipped date.
    """
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
        return render(
            request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        return redirect('products')


def order_delete_confirmation(request, order_id):
    """
    Displays a confirmation page before deleting an order.
    Deletes the order upon confirmation.
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST' and 'delete_order' in request.POST:
        # Proceed with deletion
        order.delete()
        return redirect('orders')
    return render(
        request, 'payment/order_delete_confirmation.html', {'order': order})


def no_orders_found(request):
    """
    Displays a page indicating that no orders were found for the user.
    """
    return render(request, 'payment/no_orders_found.html')


def orders_id(request, pk):
    """
    Displays detailed information,
    for a specific order and allows superusers to update the shipping status.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                Order.objects.filter(id=pk).update(
                    shipped=True, date_shipped=timezone.now())
            else:
                Order.objects.filter(id=pk).update(shipped=False)
            return redirect('not_shipped_dash')
        return render(
            request, 'payment/orders_id.html', {"order": order, "items": items})
    else:
        return redirect('home')


def orders(request):
    """
    Displays a list of orders for the logged-in user.
    Superusers see all orders, while regular users see their own.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        if not orders.exists():
            return redirect('no_orders_found')

        if request.POST:
            pk = request.POST.get('order_id')
            status = request.POST.get('shipping_status')
            if status == "true":
                Order.objects.filter(id=pk).update(
                    shipped=True, date_shipped=timezone.now())
                return redirect('orders')
            else:
                Order.objects.filter(id=pk).update(shipped=False)

            return redirect('orders')

        return render(request, 'payment/orders.html', {"orders": orders})

    else:
        return redirect('home')


def delete_order(request, order_id):
    """
    Deletes an order if the user,
    is a superuser and redirects to the orders page.
    """
    if not request.user.is_superuser:
        messages.error(
            request, "You are not authorized to delete orders.")
        return redirect('orders')

    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(
        request, f"Order #{order_id} has been successfully deleted.")
    return redirect('orders')


def send_bill(request, user, shipping_address1, total_price, order_id):
    """
    Sends an order confirmation email to the user and clears the shopping cart.
    """
    subject = 'Order Confirmation - Astro Shop'
    message = render_to_string('confirmation_emails/confirmation_email_order.txt', {
        'user': user.get_full_name() if user.first_name and user.last_name else user.username,
        'shipping_address1': shipping_address1,
        'total_price': f"{total_price:.2f} EUR",
        'order_id': order_id,
        'domain': get_current_site(request).domain,
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    # empty shopping cart
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]


def billing_info(request):
    """
    Handles the billing information process,
    including saving shipping details, creating an order,
    rendering PayPal payment form, and sending confirmation email.
    """
    billing_form = PaymentForm()
    payment_form = PaymentForm()

    if request.method == "POST":
        # Store shipping info in session
        my_shipping = {
            'shipping_full_name': request.POST.get('shipping_full_name'),
            'shipping_address1': request.POST.get('shipping_address1'),
            'shipping_address2': request.POST.get('shipping_address2'),
            'shipping_city': request.POST.get('shipping_city'),
            'shipping_state': request.POST.get('shipping_state'),
            'shipping_zipcode': request.POST.get('shipping_zipcode'),
            'shipping_country': request.POST.get('shipping_country'),
        }
        request.session['my_shipping'] = my_shipping

        # Get the cart and prepare PayPal form
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

            # Retrieve existing shipping info or create new
            shipping_address, created = ShippingAddress.objects.get_or_create(user=user)

            # Check if shipping information has changed
            if (
                shipping_address.shipping_full_name != my_shipping['shipping_full_name']
                or shipping_address.shipping_address1 != my_shipping['shipping_address1']
                or shipping_address.shipping_address2 != my_shipping['shipping_address2']
                or shipping_address.shipping_city != my_shipping['shipping_city']
                or shipping_address.shipping_state != my_shipping['shipping_state']
                or shipping_address.shipping_zipcode != my_shipping['shipping_zipcode']
                or shipping_address.shipping_country != my_shipping['shipping_country']
            ):
                # Update the shipping address in the database
                shipping_address.shipping_full_name = my_shipping['shipping_full_name']
                shipping_address.shipping_address1 = my_shipping['shipping_address1']
                shipping_address.shipping_address2 = my_shipping['shipping_address2']
                shipping_address.shipping_city = my_shipping['shipping_city']
                shipping_address.shipping_state = my_shipping['shipping_state']
                shipping_address.shipping_zipcode = my_shipping['shipping_zipcode']
                shipping_address.shipping_country = my_shipping['shipping_country']
                shipping_address.save()

            # Create Order
            create_order = Order(
                user=user,
                full_name=my_shipping['shipping_full_name'],
                email=user.email,  # Use the authenticated user's email
                shipping_address="\n".join([
                    my_shipping[key] for key in [
                        'shipping_address1',
                        'shipping_address2',
                        'shipping_city',
                        'shipping_state',
                        'shipping_zipcode',
                        'shipping_country',
                    ]
                ]),
                amount_paid=totals,
                invoice=paypal_dict['invoice'],  # Use invoice from PayPal dict
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
                    price=product.sale_price if product.is_sale else product.price,
                )
                create_order_item.save()

            # Send order confirmation email
            send_bill(
                request,
                user,
                my_shipping['shipping_address1'],
                totals,
                create_order.id,
            )

            # Payment info
            try:
                pay_user = PaymentOfPayPal.objects.get(user_paypal_id=user.id)
                payment_form = PaymentForm(instance=pay_user)
            except PaymentOfPayPal.DoesNotExist:
                payment_form = PaymentForm()  # Empty form for new user

            # Render response
            return render(
                request,
                "payment/billing_info.html",
                {
                    "paypal_form": paypal_form,
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "invoice": paypal_dict['invoice'],
                    "shipping_info": my_shipping,
                    "billing_form": billing_form,
                    "payment_form": payment_form,
                },
            )

        # If the user is not authenticated, redirect to login
        return redirect("login")

    # Handle non-POST requests
    return render(
        request,
        "payment/billing_info.html",
        {
            "billing_form": billing_form,
            "payment_form": payment_form,
        },
    )


def checkout(request):
    """
    Handles checkout process for both authenticated users and guests,
    including cart details and shipping form rendering.
    """
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )


def send_paymentOK(request, user, order_id):
    """
    Sends a confirmation email to the user after a successful payment.
    """
    subject = 'Payment OK - Astro Shop'
    message = render_to_string(
        'confirmation_emails/confirmation_paymentOK.txt', {
            'user': user.get_full_name() if user.first_name and user.last_name else user.username,
            'order_id': order_id,
            'domain': get_current_site(request).domain,
        }
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        "A confirmation email has been sent"
    )


def payment_success(request):
    """
    Handles the payment success flow, including sending confirmation email
    and clearing the cart and shipping session data.
    """
    if request.user.is_authenticated:
        user = request.user
        last_order = Order.objects.filter(user=user).order_by('-id').first()
        if last_order:
            order_id = last_order.id
            send_paymentOK(request, user, order_id)
            session_keys_to_remove = ['cart', 'my_shipping']
            for key in session_keys_to_remove:
                if key in request.session:
                    del request.session[key]
            return render(
                request, "payment/payment_success.html", {"order_id": order_id})
        else:
            messages.error(request, "No order found to confirm payment.")
            return redirect("home")
    else:
        messages.error(
            request, "You need to be logged in to complete payment.")
        return redirect("login")


def payment_failed(request):
    """
    Renders the payment failed page.
    """
    return render(request, "payment/payment_failed.html", {})
