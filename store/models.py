from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Profile(models.Model):
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
		return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)

# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'categories'



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)    
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    supplier_company_name = models.CharField(max_length=100)
    supplier_address1 = models.CharField(max_length=200, null=True, blank=True)
    supplier_address2 = models.CharField(max_length=200, null=True, blank=True)
    supplier_city = models.CharField(max_length=200, null=True, blank=True)
    supplier_state = models.CharField(max_length=200, null=True, blank=True)
    supplier_zipcode = models.CharField(max_length=200, null=True, blank=True)
    supplier_country = models.CharField(max_length=200, null=True, blank=True)
    supplier_product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.supplier_company_name


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50)

    def __str__(self):
        return self.email
        return self.date_subscribed