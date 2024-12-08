from django.contrib.sitemaps import Sitemap
from django.urls import reverse  
from .models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):        
        return ['home', 'about', 'products']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_sale=True)

    def lastmod(self, obj):
        # Ensure 'date_added' is a valid field in your Product model.
        return obj.date_added  # Replace this with the actual field you want to use.
