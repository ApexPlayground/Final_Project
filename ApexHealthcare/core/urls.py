from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

path('', views.home, name='home'),
path('register/', views.registerView, name='reg'),
path('reg_user/', views.registerUser, name='reg_user'),
path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp_page'),
path('login/', views.loginView, name='login'),
path('patient/', views.patient_home, name='patient'),
path('create_profile/', views.create_profile, name='create_profile'),
path('edit-profile/', views.profile_edit, name='edit_profile'),
path('diagnosis/', views.diagnosis, name='diagnosis'),
path('diagnosis/predict', views.MakePrediction, name='predict'),
path('result/', views.patient_result, name='result'),
path('disease_advice/', views.disease_advice, name='disease_advice'),
path('result/appointment', views.MakeAppointment, name='appointment'),
path('appointment/', views.patient_appointment, name='appointment_list'),
path('logout/', views.logoutView, name='logout'),
path('doctor/', views.doctor_home, name='doctor'),
path('save_appointment/', views.SaveAppointment, name='save_appointment'),
path('appointments/', views.doctor_appointment, name='appointments_list'),
path('remove_appointment/<int:pk>/', views.remove_appointment, name='remove_appointment'),
path('about/', views.about, name='about'),
path('doctor-login/', views.doctorLogin, name='doctor_login'),









]