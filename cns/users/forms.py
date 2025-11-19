from django import forms

ALGO_CHOICES = [
    ("CAESAR", "Caesar"),
    ("PLAYFAIR", "Playfair"),
    ("HILL", "Hill"),
]

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    algorithm = forms.ChoiceField(choices=ALGO_CHOICES)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
