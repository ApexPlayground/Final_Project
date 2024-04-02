from django.contrib import admin
from .models import User,Profile,Medical,Appointment


models_list = [User,Profile,Medical,Appointment]
admin.site.register(models_list)