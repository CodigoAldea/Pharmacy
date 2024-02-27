from django import forms
from django.forms import ModelForm,widgets
from .models import *

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'adddress', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control p-input'}),
            'adddress': forms.TextInput(attrs={'class': 'form-control p-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-control p-input'}),
        }