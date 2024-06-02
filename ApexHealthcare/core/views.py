# Import necessary modules and classes
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
import datetime
import joblib as joblib
import numpy as np
import pandas as pd
from datetime import datetime
from django.utils.timezone import now
from datetime import timedelta
from .models import User, Medical, Appointment, Profile
from .forms import UserRegistrationForm, LoginForm,ProfileCreationForm, ProfileEditForm





# Define the home view function
def home(request):
    # Render the home template
    return render(request, 'home.html')

# Define the registerView view function
def registerView(request):
    # Render the registration template
    return render(request, 'register.html')


        
def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.phonenumber = form.cleaned_data['phonenumber']  # Save the phonenumber from the form
            user.is_doctor = True
          #  user.is_doctor = True
            user.is_active = False  # Keep user inactive until email is verified
            # Generate OTP
            user.email_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.otp_created_at = timezone.now()
            user.save()
            # Send OTP via email
            send_mail(
                'Your Email Verification OTP',
                f'Your OTP is: {user.email_otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            # Redirect to OTP verification page
            return redirect('verify_otp_page', user_id=user.id)  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('reg')
        
    
def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Check if OTP is correct and not expired 
        if user.email_otp == otp and (timezone.now() - user.otp_created_at) <= timedelta(minutes=5):
            user.email_verified = True
            user.is_active = True
            user.email_otp = ''  
            user.save()
            messages.success(request, "Your email has been verified successfully. You can now login.")
            return redirect('login')  
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")

    # If GET request or OTP verification failed
    return render(request, 'verify_otp.html', {'user_id': user_id})


    
@csrf_exempt
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect based on user type
                    if hasattr(user, 'is_patient') and user.is_patient:
                        return redirect('patient')
                    elif hasattr(user, 'is_doctor') and user.is_doctor:
                        return redirect('doctor')
                    else:
                        return redirect('home')  # or some 
                else:
                    messages.info(request, "Account is inactive. Please enter otp to activate .")
                    return redirect('login')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


        
    

def patient_home(request):
    doctor = User.objects.filter(is_doctor=True).count()
    patient = User.objects.filter(is_patient=True).count()
    appointment = Appointment.objects.filter(approved=True).count()

    user_id = request.user.id
    user_profile = Profile.objects.filter(user_id=user_id)
    if not user_profile:
        context = {'profile_status':'YOU HAVE TO CREATE PROFILE TO USE OUR SERVICES', 'doctor':doctor, 'appointment':appointment, patient:'patient'}
        return render(request, 'patient/home.html', context)
    else:
        context = {'status':'1', 'doctor':doctor, 'appointment':appointment, patient:'patient'}
        return render(request, 'patient/home.html', context)
    
def create_profile(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, 'Your Profile Was Created Successfully')
            return redirect('patient')  # Redirect after successful profile creation
        else:
            print("Form errors:", form.errors)  # Log form errors if not valid
    else:
        form = ProfileCreationForm()  # If not POST, provide an empty form
    return render(request, 'patient/create_profile.html', {'form': form})
    
    
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('edit_profile')  
    else:
        form = ProfileEditForm(instance=request.user)  

    return render(request, 'patient/edit_profile.html', {'form': form})
    

def diagnosis(request):
    symptoms = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
    symptoms = sorted(symptoms)
    context = {'symptoms':symptoms, 'status':'1'}
    return render(request, 'patient/diagnosis.html', context)


@csrf_exempt
def MakePrediction(request):
    s1 = request.POST.get('s1')
    s2 = request.POST.get('s2')
    s3 = request.POST.get('s3')
    s4 = request.POST.get('s4')
    s5 = request.POST.get('s5')
    s6 = request.POST.get('s6')
    s7 = request.POST.get('s7')
    s8 = request.POST.get('s8')
    s9 = request.POST.get('s9')
    s10 = request.POST.get('s10')
    id = request.POST.get('id')

    list_b = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    print(list_b)

    list_a = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

    # Initialize list_c with zeros
    list_c = [0] * len(list_a)

    # Set symptom presence (1) based on input
    for z, symptom in enumerate(list_a):
        if symptom in list_b:
            list_c[z] = 1

    # Prepare data for prediction
    test = np.array(list_c).reshape(1, -1)

    # Load the model and prediction
    clf = joblib.load('model/final_rf_classifier.pkl')
    prediction = clf.predict(test)
    result = prediction[0]

    print('Predicted disease:', result)

    # Create a Medical instance and save to the database
    a = Medical(
        s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, 
        s6=s6, s7=s7, s8=s8, s9=s9, s10=s10, 
        disease=result, patient_id=id
    )

    # Read the disease treatment data
    disease_treatment_df = pd.read_csv('Disease_treatment.csv')

    # Check if the predicted disease is in the CSV file and retrieve treatment info
    if result in disease_treatment_df['Disease'].values:
        treatment_info = disease_treatment_df[disease_treatment_df['Disease'] == result].iloc[0]
        a.description = treatment_info['Description']
        a.diet = treatment_info['Diet']
        a.medication = treatment_info['Medication']
        precautions = [treatment_info[f'Precaution_{i+1}'] for i in range(4)]
        a.precaution = ', '.join(precautions)

    a.save()

    return JsonResponse({'status': result})







@login_required
def disease_advice(request):
    user_id = request.user.id
    disease_name = request.GET.get('disease')  # Retrieve the 'disease' from GET parameters

    if not disease_name:
        return render(request, 'patient/disease_advice.html', {'status': 'error', 'message': 'No disease specified.'})

    medical_records = Medical.objects.filter(disease=disease_name, patient_id=user_id)

    if not medical_records:
        context = {'status': 'not_found', 'message': 'No record found for this disease'}
    else:
        # Initialize sets to store unique items
        descriptions = set()
        diets = set()
        medications = set()
        precautions = set()

        for record in medical_records:
            if record.description:
                descriptions.add(record.description)
            if record.diet:
                diets.update(record.diet.split('; ')) 
            if record.medication:
                medications.update(record.medication.split('; '))  
            if record.precaution:
                precautions.update(record.precaution.split('; ')) 

        if not descriptions or not diets or not medications or not precautions:
            context = {
                'status': 'incomplete',
                'disease': disease_name,
                'message': 'Advice not available or incomplete. Please consult your doctor for more information.'
            }
        else:
            context = {
                'status': 'success',
                'disease': disease_name,
                'description': '; '.join(descriptions),
                'diet': '; '.join(diets),
                'medication': '; '.join(medications),
                'precautions': '; '.join(precautions),
            }

    return render(request, 'patient/disease_advice.html', context)



def patient_result(request):
    user_id = request.user.id
    disease = Medical.objects.all().filter(patient_id=user_id)
    context = {'disease':disease, 'status':'1'}
    return render(request, 'patient/result.html', context)
                
@csrf_exempt
def MakeAppointment(request):
    disease = request.POST.get('disease')
    userid = request.POST.get('userid')

    try:
        check_medical = Appointment.objects.filter(medical_id=disease).exists()
        if(check_medical == False):
            appointment = Appointment(medical_id=disease, patient_id=userid)
            appointment.save()
            return JsonResponse({'status':'saved'})
        else:
            print('Appointment Exist')
            return JsonResponse({'status':'exist'})
    except Exception as e:
        return JsonResponse({'status':'error'})			


def patient_appointment(request):
    user_id = request.user.id
    appointment = Appointment.objects.all().filter(patient_id=user_id)
    context = {'appointment':appointment, 'status':'1'}
    return render(request, 'patient/appointment.html', context)


def logoutView(request):
    logout(request)
    return redirect('login')   

@login_required
def doctor_home(request):
    doctor_count = User.objects.filter(is_doctor=True).count()
    patient_count = User.objects.filter(is_patient=True).count()
    appointment_count = Appointment.objects.filter(approved=True).count()
    approved_appointments = Appointment.objects.filter(approved=True)

    context = {
        'doctor': doctor_count,
        'appointment': appointment_count,
        'patient': patient_count,
        'approved_appointments': approved_appointments,
    }
    return render(request, 'doctor/home.html', context)

@login_required
def doctor_appointment(request):
    appointments = Appointment.objects.filter(approved=False)
    context = {'appointment': appointments, 'status': '1'}
    return render(request, 'doctor/appointment.html', context)


@login_required
@csrf_exempt
def SaveAppointment(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        day = request.POST.get('day')
        time = request.POST.get('time')
        user_id = request.user.id

        print(f"Received pk: {pk}, day: {day}, time: {time}, user_id: {user_id}")  # Add logging

        try:
            appointment = Appointment.objects.get(pk=pk)
            if appointment:
                appointment.approved = True
                appointment.appointment_day = day
                appointment.time = time
                appointment.doctor_id = user_id
                appointment.save()

                # Send email notification to the patient
                patient_email = appointment.patient.email
                send_mail(
                    'Appointment Approved',
                    f'Your appointment for {appointment.medical.disease} has been approved. It is scheduled for {day} at {time}.',
                    settings.EMAIL_HOST_USER,
                    [patient_email],
                    fail_silently=False,
                )

                return JsonResponse({'status': 'Appointment Set', 'approved': True})
            else:
                print('Appointment Not Exist')
                return JsonResponse({'status': 'Appointment Not Exist'}) 
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'Invalid request method'})


@login_required
@csrf_exempt
def remove_appointment(request, pk):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()
            messages.success(request, "Appointment successfully removed.")
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment does not exist.")
    return redirect('doctor')

def doctorLogin(request):
    return render(request, 'doctor.html')

def about(request):
    return render(request, 'about.html')