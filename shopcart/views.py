from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def shopcart_summary(request):
    """
    Display a summary of the shopping cart.

    Retrieves the products in the cart, their quantities, and the total price,
    and renders the 'shopcart_summary.html' template with this data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template with cart details.
    """
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "shopcart_summary.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
    })


def shopcart_add(request):
    """
    Add a product to the shopping cart.

    Retrieves product ID and quantity from a POST request, adds the product to
    the cart, and returns a JSON response with the updated cart quantity.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing,
        the cart quantity after adding the product.
    """
    # Get the cart
    cart = Cart(request)

    # Check for POST action
    if request.POST.get('action') == 'post':
        # Get product details
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product in the database
        product = get_object_or_404(Product, id=product_id)

        # Add product to the cart
        cart.add(product=product, quantity=product_qty)

        # Get the updated cart quantity
        cart_quantity = cart.__len__()

        # Display success message
        messages.success(request, f'Added {product.name} to your bag')

        # Return JSON response
        response = JsonResponse({'qty': cart_quantity})
        return response


def shopcart_delete(request):
    """
    Remove a product from the shopping cart.

    Retrieves product ID from a POST request,
    deletes the product from the cart,
    and returns a JSON response with the deleted product ID.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing,
        the product ID of the deleted product.
    """
    # Get the cart
    cart = Cart(request)

    # Check for POST action
    if request.POST.get('action') == 'post':
        # Get product ID
        product_id = int(request.POST.get('product_id'))

        # Delete product from the cart
        cart.delete(product=product_id)

        # Display warning message
        messages.warning(request, f'Item Deleted From Shopping Cart')

        # Return JSON response
        response = JsonResponse({'product': product_id})
        return response


def shopcart_update(request):
    """
    Update the quantity of a product in the shopping cart.

    Retrieves product ID and quantity from a POST request, updates the quantity
    in the cart, and returns a JSON response with the updated quantity.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing,
        the updated quantity for the product.
    """
    # Get the cart
    cart = Cart(request)

    # Check for POST action
    if request.POST.get('action') == 'post':
        # Get product details
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Update product quantity in the cart
        cart.update(product=product_id, quantity=product_qty)

        # Display success message
        messages.success(request, f'Your Cart Has Been Updated')

        # Return JSON response
        response = JsonResponse({'qty': product_qty})
        return response
