from store.models import Product, Profile

class Cart():
	def __init__(self, request):
		self.session = request.session
		
		self.request = request
		
		shopcart = self.session.get('session_key')
		
		if 'session_key' not in request.session:
			shopcart = self.session['session_key'] = {}
		
		self.shopcart = shopcart
        
	def add(self, product):
		product_id = str(product.id)

		# Logic
		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = {'price': str(product.price)}

		self.session.modified = True