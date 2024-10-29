from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time
from .models import Order

@receiver(valid_ipn_received)
def paypal_payment_recieved(sender, **kwargs):
    # timer 5 sec
    time.sleep(5)

    # Grag the info that PayPal sends
    paypal_obj = sender
    # grab the invoice
    my_Invoice = str(paypal_obj.invoice)

    # Match the invoice
    my_Order = Order.objects.get(invoice=my_Invoice)

    my_Order.paid = True

    my_Order.save()
    
    # print(paypal_obj)
    # print(f'amount paid: {paypal_obj.mc_gross} ')