__author__ = 'Elvan'
__date__ = '2017/8/13 19:39'


from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
