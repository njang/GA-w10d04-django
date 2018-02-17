from django import forms
# from django.forms import ModelForm
from .models import Treasure

# class TreasureForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=100)
#     value = forms.DecimalField(label='Value', max_digits=10, decimal_places=2)
#     material = forms.CharField(label='Material', max_length=100)
#     location = forms.CharField(label='Location', max_length=100)

class TreasureForm(forms.ModelForm):
	class Meta:
		model = Treasure
		fields = ['name', 'value', 'material', 'location']

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())