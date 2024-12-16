from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    SetPasswordForm,
)
from django import forms
from .models import Product, Profile, Subscription, Supplier


class UpdateProductForm(forms.ModelForm):
    """
    A form for updating an existing product in the database.
    Includes fields such as name, description, price, sale price,
    category, and image.
    """
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'sale_price',
            'is_sale',
            'category',
            'image',
        ]


class ProfileForm(forms.ModelForm):
    """
    A form for updating a user's profile information.
    Includes fields for address, city, state, country, phone, and more.
    """
    address1 = forms.CharField(
        label="Address 1",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
        required=False,
    )
    address2 = forms.CharField(
        label="Address 2",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
        required=False,
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=False,
    )
    state = forms.CharField(
        label="State",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=False,
    )
    zipcode = forms.CharField(
        label="Zipcode",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False,
    )
    country = forms.CharField(
        label="Country",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=False,
    )
    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            'phone',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
            'country',
        ]


class ChangePasswordForm(SetPasswordForm):
    """
    A form for allowing a user to set or change their password.
    Customizes the appearance and adds help text for the password fields.
    """
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = (
            "Your password can't be too similar to other personal information."
            "At least 8 characters."
        )

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = (
            "Enter the same password as before, for verification."
        )


class UpdateUserForm(UserChangeForm):
    """
    A form for updating a user's information (username, first name,
    last name, email). Removes the password field for better UX.
    """
    password = None
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'User Name',
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<Required. 150 characters or fewer.' +
            'Letters, digits and @/./+/-/_ only.'
        )


class SignUpForm(UserCreationForm):
    """
    A form for creating a new user account.
    Includes fields for username, first name, last name, email, and password.
    """
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'User Name',
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Required. 150 characters or fewer.' +
            'Letters, digits and @/./+/-/_ only.</small>'
            '</span>'
        )

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to '
            'your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Enter the same password as before,' +
            'for verification.</small>'
            '</span>'
        )


class SubscribeForm(forms.ModelForm):
    """
    A form for subscribing users to a newsletter or updates.
    Includes only the email field.
    """
    class Meta:
        model = Subscription
        fields = ['email']


class SupplierForm(forms.ModelForm):
    """
    A form for managing supplier information.
    Includes fields for the supplier's company name, address,
    city, state, country, and the products they supply.
    """
    class Meta:
        model = Supplier
        fields = [
            'supplier_company_name',
            'supplier_address1',
            'supplier_address2',
            'supplier_city',
            'supplier_state',
            'supplier_country',
            'supplier_zipcode',
            'supplier_product',
        ]
        widgets = {
            'supplier_product': forms.Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 15ch;',
            }),
        }
