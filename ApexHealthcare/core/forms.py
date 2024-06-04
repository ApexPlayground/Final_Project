from django import forms
from .models import User, Profile
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from datetime import datetime

# Define a form for user registration inheriting from Django's ModelForm
class UserRegistrationForm(forms.ModelForm):
    # Define form fields with password inputs
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    phonenumber = forms.CharField(required=True)

    class Meta:
        model = User  # Specify the model to use for the form
        fields = ['username', 'email', 'password', 'phonenumber']  # Fields to include in the form

    # Custom validation for email field
    def clean_email(self):
        email = self.cleaned_data['email']
        EmailValidator()(email)  # Validate email format
        # Check if the email is already taken by another user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already registered with another account.")
        return email

    # Custom validation for username field
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    # Custom validation for the entire form
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Ensure both password and confirm_password are present and match
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Password and Confirm Password do not match")
        return cleaned_data

# Define a login form with username and password fields
class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Define a form for creating a profile, inheriting from Django's ModelForm
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile  # Specify the model to use for the form
        fields = ['birth_date', 'gender', 'country', 'avatar']  # Fields to include in the form
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }

    # Custom validation for birth_date field
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if (datetime.today().date() - birth_date).days / 365.25 < 18:
            raise forms.ValidationError("You are under 18. Please visit a doctor for your diagnosis.")
        return birth_date

# Define a form for editing a profile, inheriting from Django's ModelForm
class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User  # Specify the model to use for the form
        fields = ['username', 'email', 'phonenumber', 'avatar']  # Fields to include in the form

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

    # Custom validation for email field
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already registered with another account.")
        return email
