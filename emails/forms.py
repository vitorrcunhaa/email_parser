from django import forms
from .models import EmailData


class EmailDataForm(forms.ModelForm):
    class Meta:
        model = EmailData
        fields = ['name', 'amount', 'comments']
