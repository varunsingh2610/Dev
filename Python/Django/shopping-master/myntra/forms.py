from django import forms

class ProductForm(forms.Form):
    id = forms.CharField(label='Product ID')
    url = forms.CharField(label='Product URL')
