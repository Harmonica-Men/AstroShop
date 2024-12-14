from django.urls import reverse

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Profile(models.Model):
    """
    Represents a user profile associated with a Django User model.

    Attributes:
        user (User): A one-to-one relationship with the User model.
        date_modified (DateTimeField): The last modified timestamp for the
            profile.
        phone (CharField): The phone number of the user.
        address1 (CharField): The primary address of the user.
        address2 (CharField): An additional address line.
        city (CharField): The city of the user.
        state (CharField): The state of the user.
        zipcode (CharField): The postal code of the user.
        country (CharField): The country of the user.
        old_cart (CharField): Stores the previous cart information (optional).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """Returns the username associated with the profile."""
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a Profile when a new User is created.

    Args:
        sender: The model class sending the signal.
        instance: The instance of the sender model.
        created (bool): True if a new instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# Automate the profile creation process
post_save.connect(create_profile, sender=User)


class Category(models.Model):
    """
    Represents a category for products.

    Attributes:
        name (CharField): The name of the category.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False, default='default-slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns the name of the category."""
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    """
    Represents a product in the system.

    Attributes:
        name (CharField): The name of the product.
        price (DecimalField): The price of the product.
        category (ForeignKey): The category to which the product belongs
            (optional).
        description (TextField): A description of the product.
        image (ImageField): The image of the product.
        is_sale (BooleanField): Whether the product is on sale.
        sale_price (DecimalField): The sale price of the product
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField(default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    date_added = models.DateTimeField(
        auto_now_add=True)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        """Returns the name of the product."""
        return self.name

    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        pass


class Supplier(models.Model):
    """
    Represents a supplier of products.

    Attributes:
        supplier_company_name (CharField): The name of the supplier company.
        supplier_address1 (CharField): The primary address of the supplier.
        supplier_address2 (CharField): An additional address line.
        supplier_city (CharField): The city of the supplier.
        supplier_state (CharField): The state of the supplier.
        supplier_zipcode (CharField): The postal code of the supplier.
        supplier_country (CharField): The country of the supplier.
        supplier_product (OneToOneField): The product supplied by the supplier.
    """
    supplier_company_name = models.CharField(max_length=100)
    supplier_address1 = models.CharField(max_length=200, null=True, blank=True)
    supplier_address2 = models.CharField(max_length=200, null=True, blank=True)
    supplier_city = models.CharField(max_length=200, null=True, blank=True)
    supplier_state = models.CharField(max_length=200, null=True, blank=True)
    supplier_zipcode = models.CharField(max_length=200, null=True, blank=True)
    supplier_country = models.CharField(max_length=200, null=True, blank=True)
    supplier_product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        """Returns the name of the supplier company."""
        return self.supplier_company_name


class Subscription(models.Model):
    """
    Represents a subscription for receiving updates or newsletters.

    Attributes:
        email (EmailField): The email address of the subscriber.
        is_confirmed (BooleanField): Indicate if the subscription is confirmed.
        confirmation_code (CharField): The unique confirmation code for the
            subscription.
    """
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50)

    def __str__(self):
        """Returns the email of the subscriber."""
        return self.email
