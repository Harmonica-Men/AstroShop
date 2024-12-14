from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductSitemap(Sitemap):
    """Sitemap for products in the catalog."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        """Retrieve all Product objects for the sitemap."""
        return Product.objects.all()

    def lastmod(self, obj):
        """
        Get the last modification date for a product.

        Returns:
            The 'updated' field of the product if available, otherwise None.
        """
        return obj.updated if hasattr(obj, "updated") else None
