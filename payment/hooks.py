from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings

# @receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    paypal_obj = sender
    print(paypal_obj)
    print(f'amount Paid: {paypal_obj.mc_gross}')
