
from django import forms
from .models import Product, CustomerOrder


# =====================================
# PRODUCT FORM
# =====================================
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'price',
            'quantity',
            'supplier',
            'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price',
                'min': '0',
                'step': '0.01'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter available quantity',
                'min': '0'
            }),

            'supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


# =====================================
# CUSTOMER ORDER FORM
# =====================================
class CustomerOrderForm(forms.ModelForm):

    class Meta:
        model = CustomerOrder

        fields = [
            'customer_name',
            'customer_location',
            'contact_number',
            'social_media_account',
            'product',
            'quantity'
        ]

        labels = {
            'customer_name': 'Customer Name',
            'customer_location': 'Customer Location',
            'contact_number': 'Contact Number',
            'social_media_account': 'Social Media Account',
            'product': 'Select Product',
            'quantity': 'Order Quantity'
        }

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer full name'
            }),

            'customer_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer address'
            }),

            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number'
            }),

            'social_media_account': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Facebook name or account link'
            }),

            'product': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
                'min': '1'
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if quantity < 1:
            raise forms.ValidationError(
                'Quantity must be at least 1.'
            )

        return quantity
