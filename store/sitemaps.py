from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product, Category

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['index', 'about', 'contact']  # Add your static views' names

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_sale=True)  # Include only sale items or customize logic

    def lastmod(self, obj):
        return obj.updated_at  # Assuming you have an `updated_at` field in the Product model

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all()
