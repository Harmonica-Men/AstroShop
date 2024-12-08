from django.contrib.sitemaps import Sitemap
from django.urls import reverse  # Correct import
from .models import Product, Category

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):        
        return ['home', 'about', 'category', 'products']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_sale=True)  

    def lastmod(self, obj):
        return obj.updated_at  

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):    
        return Category.objects.all()

    def location(self, item):    
        return reverse('category', args=[item.slug]) 
