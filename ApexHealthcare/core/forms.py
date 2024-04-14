from django import forms
from .models import User,Profile
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from datetime import datetime

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    phonenumber = forms.CharField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phonenumber']  

    def clean_email(self):
        email = self.cleaned_data['email']
        EmailValidator()(email)
        # Check if the email is taken by another user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already registered with another account.")
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

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender', 'country', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender', 'country', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if (datetime.today().date() - birth_date).days / 365.25 < 18:
            raise forms.ValidationError("You are under 18. Please visit a doctor for your diagnosis.")
        return birth_date

class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phonenumber', 'avatar']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Initialize the form with the instance's profile image if it exists
        if self.instance.profile:
            self.fields['avatar'].initial = self.instance.profile.avatar

    def save(self, *args, **kwargs):
        # Save the User info
        user = super(ProfileEditForm, self).save(*args, **kwargs)
        # Save or update the profile image
        profile, created = Profile.objects.update_or_create(
            user=user,
            defaults={'avatar': self.cleaned_data.get('avatar')}
        )
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already registered with another account.")
        return email

