from django import forms

class CustPhone(forms.Form):
    # Define an IntegerField in your form
    phone = forms.IntegerField(label='Customer Phone',widget=forms.TextInput(attrs={'class': 'form-control p-input'}),required=False)

class CustName(forms.Form):
    # Define an IntegerField in your form
    name = forms.CharField(max_length=150,label='Customer Name',widget=forms.TextInput(attrs={'class': 'form-control p-input'}))
class DateForm(forms.Form):
    # Define an IntegerField in your form
    date_start = forms.DateField(label='Date-Start',widget=forms.TextInput(attrs={'class': 'form-control p-input','type':'date'}),required=False)
    date_end = forms.DateField(label='Date-End',widget=forms.TextInput(attrs={'class': 'form-control p-input','type':'date'}),required=False)