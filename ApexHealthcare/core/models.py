from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
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
    # Symptoms fields
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)
    s4 = models.CharField(max_length=200)
    s5 = models.CharField(max_length=200)
    
    disease = models.CharField(max_length=200)  # Field to store the diagnosed disease
    medicine = models.CharField(max_length=200)  # Field to store prescribed medicine
    
    patient = models.ForeignKey(User, related_name="medical_history", on_delete=models.CASCADE)  # ForeignKey for patient
    doctor = models.ForeignKey(User, related_name="prescriptions", on_delete=models.CASCADE, null=True)  # ForeignKey for doctor
    created_on = models.DateTimeField(auto_now_add=True)  # Field to store the creation date of the record

    def __str__(self):
        return self.disease  # String representation of the Medical record, returns the disease name

class Appointment(models.Model):
    # Indicates if the appointment is approved
    approved = models.BooleanField(default=False)  
    # Field to store the time of the appointment
    time = models.CharField(max_length=200, null=True)  
    # ForeignKey for patient, related name "patient_appointment"
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)  
     # ForeignKey for doctor, related name "doctor_appointment"
    doctor = models.ForeignKey(User, related_name="doctor_appointment", on_delete=models.CASCADE, null=True) 
     # Field to store the date of the appointment
    appointment_day = models.DateTimeField(null=True) 
      # ForeignKey for medical record, related name "related_medical_record"
    medical = models.ForeignKey(Medical, related_name="related_medical_record", on_delete=models.CASCADE, null=True)
     # Field to store the creation date of the appointment
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.approved  # String representation of the Appointment, returns the value of "approved"



class Profile(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # Field to store the user's avatar image
    avatar = models.ImageField(upload_to='', default='profile/avatar.png', blank=True) 
    birth_date = models.DateField(default='None')  # Field to store the user's birth date
    gender = models.CharField(max_length=255)  # Field to store the user's gender
    # Field to store the user's country, default is set to Ireland
    country = models.CharField(max_length=255, default='Ireland')  

    def __str__(self):
        return self.country  # String representation of the Profile, returns the country name
