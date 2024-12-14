from django import forms
from django.core.exceptions import ValidationError
from .models import ShippingAddress, PaymentOfPayPal
import re


# Validators for card number and CVV
def validate_card_number(value):
    """Ensure card number is exactly 16 digits."""
    if not re.fullmatch(r'\d{16}', value):
        raise ValidationError("Card number must be 16 digits.")


def validate_cvv(value):
    """Ensure CVV is 3 or 4 digits."""
    if not re.fullmatch(r'\d{3,4}', value):
        raise ValidationError("CVV must be 3 or 4 digits.")


class PaymentForm(forms.ModelForm):
    """
    A form for collecting and validating billing,
    address, and credit card details,
    including the cardholder's
    name, number, expiration date, CVV,
    and billing address information.
    """
    card_name = forms.CharField(
        label="Card Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Name on the Card'}),
        required=True
    )
    card_number = forms.CharField(
        label="Card Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Card Numbers'}),
        validators=[validate_card_number],
        required=True
    )
    card_exp_date = forms.CharField(
        label="Card Expiry",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YYYY'}),
        required=True
    )
    card_cvv_number = forms.CharField(
        label="CVV Code",
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'CVV Code'}),
        validators=[validate_cvv],
        help_text="3 or 4 digits on the back of your card.",
        required=True
    )
    card_address1 = forms.CharField(
        label="Address 1",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing Address 1'}),
        required=True
    )
    card_address2 = forms.CharField(
        label="Address 2",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing Address 2'}),
        required=False
    )
    card_city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing City'}),
        required=True
    )
    card_state = forms.CharField(
        label="State",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing State'}),
        required=True
    )
    card_zipcode = forms.CharField(
        label="Zipcode",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing Zipcode'}),
        required=True
    )
    card_country = forms.CharField(
        label="Country",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Billing Country'}),
        required=True
    )

    class Meta:
        model = PaymentOfPayPal
        fields = [
            'card_name',
            'card_number',
            'card_exp_date',
            'card_cvv_number',
            'card_address1',
            'card_address2',
            'card_city',
            'card_state',
            'card_zipcode',
            'card_country'
        ]


class ShippingForm(forms.ModelForm):
    """
    A form for collecting and validating a user's shipping address information,
    including fields like name, address,
    city, state, zipcode, and country.
    """
    shipping_full_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Full Name'}),
        required=False
    )
    shipping_address1 = forms.CharField(
        label="Address 1",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Address1'}),
        required=False
    )
    shipping_address2 = forms.CharField(
        label="Address 2",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Address2'}),
        required=False
    )
    shipping_city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'City'}),
        required=False
    )
    shipping_state = forms.CharField(
        label="State",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'State'}),
        required=False
    )
    shipping_zipcode = forms.CharField(
        label="Zip Code",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False
    )
    shipping_country = forms.CharField(
        label="Country",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Country'}),
        required=False
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_state',
            'shipping_zipcode',
            'shipping_country'
        ]
        exclude = ['user', ]
