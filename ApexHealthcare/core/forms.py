from django import forms
from .models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    phonenumber = forms.CharField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phonenumber']  # Include phonenumber in the fields

    def clean_email(self):
        email = self.cleaned_data['email']
        EmailValidator()(email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Ensure both password and confirm_password are present and match
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Password and Confirm Password do not match")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)