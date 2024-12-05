from store.models import Product, Profile


class Cart:
    """
    A shopping cart class that provides methods for managing a user's cart
    stored in the session or, if authenticated, saved in the user's profile.

    Attributes:
        session: The user's session object.
        request: The HTTP request object.
        cart: The cart stored in the session as a dictionary.
    """

    def __init__(self, request):
        """
        Initialize the cart object.

        If the user doesn't have a cart in their session,
        a new cart is created.

        Args:
            request: The HTTP request object.
        """
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        # Create a new cart if one doesn't exist
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        """
        Add a product to the cart and save it,
        in the user's profile if authenticated.

        Args:
            product (int): The ID of the product.
            quantity (int): The quantity of the product to add.
        """
        product_id = str(product)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Save the cart to the user's profile if authenticated
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        """
        Add a product to the cart.

        Args:
            product: The product instance to add.
            quantity (int): The quantity of the product to add.
        """
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Save the cart to the user's profile if authenticated
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        """
        Calculate the total price of all items in the cart.

        Returns:
            float: The total price of the cart.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total

    def __len__(self):
        """
        Get the number of unique items in the cart.

        Returns:
            int: The number of unique items.
        """
        return len(self.cart)

    def get_prods(self):
        """
        Retrieve the products in the cart from the database.

        Returns:
            QuerySet: A QuerySet of products in the cart.
        """
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        """
        Get the quantities of each product in the cart.

        Returns:
            dict: A dictionary of product IDs and their quantities.
        """
        return self.cart

    def update(self, product, quantity):
        """
        Update the quantity of a product in the cart.

        Args:
            product (int): The ID of the product.
            quantity (int): The new quantity of the product.

        Returns:
            dict: The updated cart.
        """
        product_id = str(product)
        product_qty = int(quantity)
        self.cart[product_id] = product_qty
        self.session.modified = True

        # Save the cart to the user's profile if authenticated
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))

        return self.cart

    def delete(self, product):
        """
        Remove a product from the cart.

        Args:
            product (int): The ID of the product to remove.
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Save the cart to the user's profile if authenticated
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=str(carty))
