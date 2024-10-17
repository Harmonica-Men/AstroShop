from store.models import Product

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
		if product_id in self.shopcart:
			pass
		else:
			self.shopcart[product_id] = {'price': str(product.price)}

		self.session.modified = True

	def __len__(self):
		return len(self.shopcart)

	def get_prods(self):
		product_ids = self.shopcart.keys()
		products = Product.objects.filter(id__in=product_ids)
		return products
