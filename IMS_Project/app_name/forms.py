
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
            'supplier'
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
            'product',
            'quantity'
        ]

        labels = {
            'customer_name': 'Customer Name',
            'customer_location': 'Customer Location',
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
