from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# Custom User model with additional fields for patient and doctor roles
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)  # is a patient
    is_doctor = models.BooleanField(default=False)  # is a doctor
    phonenumber = models.CharField(max_length=200, null=True)  # Phone number
    email_verified = models.BooleanField(default=False)  # Email verification status
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    verification_token = models.CharField(max_length=100, blank=True, editable=False)  # Email verification token

    def save(self, *args, **kwargs):
        if not self.verification_token:
            # Generate a unique verification token
            self.verification_token = get_random_string(length=32)
        super(User, self).save(*args, **kwargs)

# Medical model to store medical records and prescriptions
class Medical(models.Model):
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    s6 = models.CharField(max_length=200, blank=True, null=True)
    s7 = models.CharField(max_length=200, blank=True, null=True)
    s8 = models.CharField(max_length=200, blank=True, null=True)
    s9 = models.CharField(max_length=200, blank=True, null=True)
    s10 = models.CharField(max_length=200, blank=True, null=True)
    disease = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    diet = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    precaution = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(User, related_name="medical_history", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="prescriptions", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease

class Appointment(models.Model):
    approved = models.BooleanField(default=False)
    time = models.CharField(max_length=200, null=True)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor_appointment", on_delete=models.CASCADE, null=True)
    appointment_day = models.DateTimeField(null=True)
    medical = models.ForeignKey(Medical, related_name="related_medical_record", on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.approved)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles/', default='profile/avatar.png', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, default='Ireland')

    def __str__(self):
        return self.country
