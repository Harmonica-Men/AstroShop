from django import template

register = template.Library()

@register.filter
def get_quantity(quantities, product_id):
    """Retrieve quantity based on the product ID."""
    return quantities.get(str(product_id), 0)

@register.filter
def calculate_subtotal(product, quantities):
    """Calculates subtotal by multiplying product price or sale price by quantity."""
    quantity = quantities.get(str(product.id), 0)
    price = product.sale_price if product.is_sale else product.price
    return price * quantity