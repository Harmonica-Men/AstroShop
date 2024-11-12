from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UpdateProductForm, ProfileForm
from django.db.models.functions import Lower
from payment.forms import ShippingForm
from payment.models import ShippingAddress, PaymentOfPayPal
from django import forms
from django.db.models import Q
import json
from shopcart.cart import Cart
from .models import Product
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def add_to_cart(request, product_id):
    # Your logic to add the product to the cart here

    # Set a success message
    messages.success(request, "Product has been added to your cart!")
    return redirect('cart')  # Redirect to a relevant page after adding to the cart


def all_products(request):
    """ A view to show all products, including sorting """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_categories': categories,
        'current_sorting': current_sorting,
	  }
    return render(request, 'products.html', context)


def index(request):
    """ A view to return the index page """
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == "POST":
        form = UpdateProductForm(request.POST, request.FILES)  # We use UpdateProductForm to add new products as well
		
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('products')  # Redirect to home or any other page after adding the product
    else:
        form = UpdateProductForm()
    return render(request, 'add_product.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product', pk=product.pk)
    else:
        form = UpdateProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})


def delete_product_confirmation(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'delete_product_confirm.html', {'product': product})


def delete_product(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Product has been deleted successfully.")
        return redirect('products')  # Redirect to home or any other page after deletion
    else:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('products')

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	


def update_user_profile(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        
        
        # Get Current User's profile Info with error handling
        try:
            
            user_profile = Profile.objects.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            user_profile = None  # Optional: handle missing profile here
            
        # Get original User Form
        form = ProfileForm(request.POST or None, instance=current_user)
        
        # Initialize profile form using the existing profile or None
        profile_form = ProfileForm(request.POST or None, instance=user_profile)
        
        if form.is_valid() and profile_form.is_valid():
            # Save forms if valid
            form.save()            
            if user_profile:  # If profile exists, update it
                profile_form.save()
            else:  # If profile doesn't exist, create a new one
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
          
            return redirect('products')
        
        return render(request, "update_user_profile.html", {'form': form, 'profile_form': profile_form})
    
    else:

        return redirect('home')


def update_ship_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        
        # Get Current User's Shipping Info with error handling
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = None  # Optional: handle missing shipping address here
            
        # Get original User Form
        form = ProfileForm(request.POST or None, instance=current_user)
        
        # Get User's Shipping Form (use an empty instance if shipping_user is None)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() and shipping_form.is_valid():
            # Save forms if valid
            form.save()
            if shipping_user:
                shipping_form.save()
            else:               
                shipping_user = shipping_form.save(commit=False)
                shipping_user.user = request.user
                shipping_user.save()

            return redirect('products')
        
        return render(request, "update_ship_profile.html", {'form': form, 'shipping_form': shipping_form})
    
    else:
        return redirect('home')

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):

					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:

		return redirect('home')

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)

			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:

		return redirect('home')

def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    
    # Check if the requested category is "Sales"
    if foo.lower() == "sales":
        # Filter for products on sale
        products = Product.objects.filter(is_sale=True)  # Using is_sale field
        category_name = "Sales"  # Set category name for display
    else:
        # Regular category handling
        try:
            category = Category.objects.get(name=foo)
            products = Product.objects.filter(category=category)
            category_name = category.name
        except Category.DoesNotExist:
            messages.success(request, "That Category Doesn't Exist...")
            return redirect('home')
    
    # Render the category page with the list of products and category name
    return render(request, 'category.html', {
        'products': products,
        'category': category_name,
        'is_sales': (foo.lower() == "sales")  # Pass is_sales as True if it's the "Sales" category
    })


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})