from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime


class PaymentOfPayPal(models.Model):
    """
    Stores the payment details of a user for PayPal transactions.
    Each user can have only one associated PayPal payment record.
    """
    user_paypal = models.OneToOneField(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19)
    card_exp_date = models.CharField(max_length=5)
    card_cvv_number = models.CharField(max_length=4)
    card_address1 = models.CharField(max_length=200)
    card_address2 = models.CharField(max_length=200, blank=True, null=True)
    card_city = models.CharField(max_length=200)
    card_state = models.CharField(max_length=200)
    card_zipcode = models.CharField(max_length=200)
    card_country = models.CharField(max_length=200)

    class Meta:
        """
        Meta class to set the plural form of the model name.
        """
        verbose_name_plural = "Payment PayPal"

    def __str__(self):
        """
        Returns a string representation of the PaymentOfPayPal object,
        displaying the user's card name.
        """
        return f"Payment PayPal details for {self.card_name}"


class ShippingAddress(models.Model):
    """
    Represents a user's shipping address for order fulfillment.
    Each address is associated with a user.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=200)
    shipping_state = models.CharField(max_length=200, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=200, null=True, blank=True)
    shipping_country = models.CharField(max_length=200)

    class Meta:
        """
        Meta class to set the plural form of the model name.
        """
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        """
        Returns a string representation of the ShippingAddress object,
        displaying the associated user's name.
        """
        return f'Shipping Address - {str(self.user)}'


def create_shipping(sender, instance, created, **kwargs):
    """
    Signal handler to automatically,
    create a shipping address when a new user is created.
    This function is triggered when a new user is saved.
    """
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


# Connect the create_shipping function,
# to the post_save signal for the User model
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    """
    Represents an order made by a user,
    including shipping and payment information.
    Each order can have multiple items associated with it.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)
    invoice = models.CharField(max_length=200, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the Order object,
        displaying the order ID and the associated user.
        """
        return f'Order # {str(self.id)} from {str(self.user)}'


@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    """
    Signal handler to automatically,
    set the shipping date when an order's status changes to shipped.
    This function is triggered before an order is saved,
    if the order's shipped status is updated.
    """
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


class OrderItem(models.Model):
    """
    Represents an individual item in an order, including the product,
    quantity, and price.
    Each order item is associated with a specific order and product.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        """
        Returns a string representation of the OrderItem object,
        displaying the order item's ID.
        """
        return f'Order Item - {str(self.id)}'
