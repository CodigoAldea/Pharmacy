# forms.py
from django import forms
from .models import YourModel
from import_export.forms import ImportForm


class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = '__all__'

class MyImportForm(ImportForm):
    import_file = forms.FileField(label='Select a file')