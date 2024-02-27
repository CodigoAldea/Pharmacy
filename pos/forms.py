from django import forms
from django.forms import ModelForm,widgets
from .models import *

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['invoice_no']
        widgets = {
            # 'date': forms.TextInput(attrs={'class': 'form-control p-input','type':'date','id':'dateInput','list':'datalist'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control p-input'}),
            
        }
class ReturnPurchaseForm(forms.Form):
        medicine_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control p-input', 'list': 'datalistOptions2'})
    )
        batch_id = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-control p-input', 'list': 'datalistOptions3'})
    )