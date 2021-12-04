from django import forms
from dataProcessor.models import ConnectionsDB


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = ConnectionsDB
        fields = ["database", "server", "username", "password"]
        widgets = {
            "database": forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            "server": forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            "username": forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
            "password": forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'off','data-toggle':'password'})
        }
