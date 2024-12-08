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
        return obj.updated_at  

