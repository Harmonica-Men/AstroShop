from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .forms import PaymentOfPayPalForm

def send_bill(request, user, shipping_address1, total_price, order_id):
    """
    Sends an order confirmation email,
    to the user after a successful order creation.
    Also empties the shopping cart session data after the order is placed.
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

    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]


def billing_info(request):
    """
    Handles the billing information page for a user,
    including PayPal integration.
    Creates or updates a shipping address, creates an order,
    and sends a confirmation email.
    """
    billing_form = PaymentForm()
    payment_form = PaymentForm()

    if request.method == "POST":
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

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Book Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'EUR',
            'notify_url': f'https://{host}{reverse("paypal-ipn")}',
            'return_url': f'https://{host}{reverse("payment_success")}',
            'cancel_return': f'https://{host}{reverse("payment_failed")}',
        }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        if request.user.is_authenticated:
            user = request.user
            shipping_address, created = ShippingAddress.objects.get_or_create(user=user)

            if (
                shipping_address.shipping_full_name != my_shipping['shipping_full_name']
                or shipping_address.shipping_address1 != my_shipping['shipping_address1']
                or shipping_address.shipping_address2 != my_shipping['shipping_address2']
                or shipping_address.shipping_city != my_shipping['shipping_city']
                or shipping_address.shipping_state != my_shipping['shipping_state']
                or shipping_address.shipping_zipcode != my_shipping['shipping_zipcode']
                or shipping_address.shipping_country != my_shipping['shipping_country']
            ):
                shipping_address.shipping_full_name = my_shipping['shipping_full_name']
                shipping_address.shipping_address1 = my_shipping['shipping_address1']
                shipping_address.shipping_address2 = my_shipping['shipping_address2']
                shipping_address.shipping_city = my_shipping['shipping_city']
                shipping_address.shipping_state = my_shipping['shipping_state']
                shipping_address.shipping_zipcode = my_shipping['shipping_zipcode']
                shipping_address.shipping_country = my_shipping['shipping_country']
                shipping_address.save()

            user_profile, created = Profile.objects.get_or_create(user=user)
            if user_profile.is_subscribed:
                profile_date = user_profile.date_subscribed.strftime('%Y-%m-%d')
            else:
                profile_date = "N/A"

            if request.method == 'POST':
                order = Order(
                    user=user,
                    shipping_address=shipping_address,
                    total=totals,
                    date_ordered=timezone.now(),
                    profile_date_subscribed=profile_date
                )
                order.save()
                send_bill(
                    request, user, shipping_address.shipping_address1, totals, order.id)
                return render(
                    request, 'payment/payment_success.html', {'paypal_form': paypal_form})
        else:
            return render(
                request, 'payment/billing_info.html', {'paypal_form': paypal_form})
    return render(
        request, 'payment/billing_info.html', {'paypal_form': paypal_form})
