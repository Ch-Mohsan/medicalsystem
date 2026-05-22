from pyexpat.errors import messages
from django.shortcuts import render, redirect
from datetime import date
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Doctor, Patient,Specialization,TimeSlot,Appointment,Review
from .forms import ContactForm
from django.db import transaction
from django.conf import settings
import requests
import secrets
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TimeSlotSerializer, AppointmentSerializer

# Home and Public Pages

def index(request):
    # Get top rated doctors with their average rating and review count
    top_doctors = Doctor.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).order_by('-avg_rating')[:3]
    
    # Get all specializations for the dropdown
    specializations = Specialization.objects.all()
    
    context = {
        'top_doctors': top_doctors,
        'specializations': specializations,
    }
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Form Submitted Successfully')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below')
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def doctors(request):
    # Annotate doctors with calculated average rating and review count from Review model and Only show doctors with complete profiles (all required fields filled)
    doctors = Doctor.objects.filter(
        specialization__isnull=False,
        license_number__isnull=False,
        clinic_address__isnull=False,
        qualification__isnull=False
    ).exclude(
        license_number='',
        clinic_address='',
        qualification=''
    ).annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    
    # Get query parameters
    name = request.GET.get('name', '').strip()
    specialization = request.GET.get('specialization', '').strip()
    min_rating = request.GET.get('min_rating', '').strip()
    fee_range = request.GET.get('fee', '').strip()
    exp_range = request.GET.get('experience', '').strip()
    sort_by = request.GET.get('sort_by', '').strip()
    
    # Filter by name (search in first name, last name, or full name)
    if name:
        # Split the search term into words for better matching
        name_words = name.split()
        name_query = Q()
        
        # Search for each word in first or last name
        for word in name_words:
            name_query &= (Q(user__first_name__icontains=word) | Q(user__last_name__icontains=word))
        
        # Also search the full name as-is in case it's in one field
        name_query |= Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name)
        
        doctors = doctors.filter(name_query)
    
    # Filter by specialization
    if specialization:
        doctors = doctors.filter(specialization__name__iexact=specialization)
    
    # Filter by minimum rating (using calculated average)
    if min_rating:
        try:
            min_rating_float = float(min_rating)
            doctors = doctors.filter(avg_rating__gte=min_rating_float)
        except ValueError:
            pass
    
    # Filter by fee range
    if fee_range == 'under_5000':
        doctors = doctors.filter(consultation_fee__lt=5000)
    elif fee_range == '5000_10000':
        doctors = doctors.filter(consultation_fee__gte=5000, consultation_fee__lte=10000)
    elif fee_range == '10000_15000':
        doctors = doctors.filter(consultation_fee__gte=10000, consultation_fee__lte=15000)
    elif fee_range == '15000_plus':
        doctors = doctors.filter(consultation_fee__gt=15000)
    
    # Filter by experience range
    if exp_range == '0_5':
        doctors = doctors.filter(experience_years__lte=5)
    elif exp_range == '5_10':
        doctors = doctors.filter(experience_years__gt=5, experience_years__lte=10)
    elif exp_range == '10_plus':
        doctors = doctors.filter(experience_years__gt=10)
    
    # Sort doctors (using calculated average rating)
    if sort_by == 'rating_high':
        doctors = doctors.order_by('-avg_rating')
    elif sort_by == 'rating_low':
        doctors = doctors.order_by('avg_rating')
    elif sort_by == 'experience_high':
        doctors = doctors.order_by('-experience_years')
    elif sort_by == 'experience_low':
        doctors = doctors.order_by('experience_years')
    elif sort_by == 'fee_low':
        doctors = doctors.order_by('consultation_fee')
    elif sort_by == 'fee_high':
        doctors = doctors.order_by('-consultation_fee')
    else:
        # Default sorting by rating (highest first)
        doctors = doctors.order_by('-avg_rating')
    
    # Get all specializations for the dropdown
    specializations = Specialization.objects.all()
    
    return render(request, 'doctors.html', {
        'doctors': doctors,
        'specializations': specializations,
        'search_params': {
            'name': name,
            'specialization': specialization,
            'min_rating': min_rating,
            'fee': fee_range,
            'experience': exp_range,
            'sort_by': sort_by,
        }
    })

@login_required(login_url='login')
def appointments(request):
    if request.user.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-appointment_date')
        return render(request, 'doctor_appointments.html', {'appointments': appointments})
    elif request.user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('-appointment_date')
        return render(request, 'patient_appointments.html', {'appointments': appointments})
    return redirect('index')

@login_required(login_url='login')
def profile(request):
    from .forms import UserForm, DoctorProfileForm, PatientProfileForm
    from django.db.models import Avg, Count
    
    user = request.user
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        
        if request.user.user_type == 'doctor':
            doctor_form = DoctorProfileForm(request.POST, instance=user.doctor)
            
            if user_form.is_valid() and doctor_form.is_valid():
                user_form.save()
                doctor_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
                
        elif request.user.user_type == 'patient':
            patient_form = PatientProfileForm(request.POST, instance=user.patient)
            
            if user_form.is_valid() and patient_form.is_valid():
                user_form.save()
                patient_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
    
    # GET request - initialize forms
    if request.user.user_type == 'doctor':
        user_form = UserForm(instance=user)
        doctor_form = DoctorProfileForm(instance=user.doctor)
        
        # Calculate doctor statistics
        rating_data = Review.objects.filter(doctor=user.doctor).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        
        # Get unique patient count from completed appointments
        total_patients = Appointment.objects.filter(
            doctor=user.doctor,
            status='completed'
        ).values('patient').distinct().count()
        
        time_slots = user.doctor.time_slots.all()
        
        context = {
            'user_form': user_form,
            'doctor_form': doctor_form,
            'time_slots': time_slots,
            'avg_rating': rating_data['avg_rating'] or 0,
            'review_count': rating_data['review_count'],
            'total_patients': total_patients,
        }
        return render(request, 'doctor_profile.html', context)
        
    elif request.user.user_type == 'patient':
        from datetime import date
        user_form = UserForm(instance=user)
        patient_form = PatientProfileForm(instance=user.patient)
        
        # Calculate patient statistics
        patient = user.patient
        total_appointments = Appointment.objects.filter(patient=patient).count()
        upcoming_appointments = Appointment.objects.filter(
            patient=patient,
            status__in=['pending', 'confirmed'],
            appointment_date__gte=date.today()
        ).count()
        
        context = {
            'user_form': user_form,
            'patient_form': patient_form,
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments,
        }
        return render(request, 'patient_profile.html', context)
        
    return redirect('index')

def doctor_detail(request, id):
    from django.db.models import Avg
    doctor = Doctor.objects.get(id=id)
    
    # Get all reviews for this doctor
    reviews = Review.objects.filter(doctor=doctor).select_related('patient__user').order_by('-id')
    
    # Calculate average rating and count
    review_stats = reviews.aggregate(avg_rating=Avg('rating'), count=Count('id'))
    avg_rating = review_stats['avg_rating'] or 0.0
    review_count = review_stats['count']
    
    # Check if logged-in user is a patient and has appointments with this doctor
    can_review = False
    has_reviewed = False
    
    if request.user.is_authenticated and request.user.user_type == 'patient':
        # Check if patient has any confirmed or completed appointments with this doctor
        has_appointment = Appointment.objects.filter(
            patient=request.user.patient,
            doctor=doctor,
            status__in=['confirmed', 'pending']
        ).exists()
        
        # Check if patient has already reviewed this doctor
        has_reviewed = Review.objects.filter(
            patient=request.user.patient,
            doctor=doctor
        ).exists()
        
        can_review = has_appointment and not has_reviewed
    
    context = {
        'doctor': doctor,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': review_count,
        'can_review': can_review,
        'has_reviewed': has_reviewed,
    }
    
    return render(request, 'doctor_detail.html', context)

@login_required(login_url='login')
def patient_detail(request, id):
    try:
        patient = Patient.objects.get(id=id)
        return render(request, 'patient_detail.html', {'patient': patient})
    except Patient.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('appointments')

@login_required(login_url='login')
def add_review(request, id):
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can leave reviews.')
        return redirect('doctor_detail', id=id)
    
    if request.method != 'POST':
        return redirect('doctor_detail', id=id)
    
    try:
        doctor = Doctor.objects.get(id=id)
        patient = request.user.patient
        
        # Check if patient has appointment with this doctor
        has_appointment = Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            status__in=['confirmed', 'pending']
        ).exists()
        
        if not has_appointment:
            messages.error(request, 'You need to book an appointment first to add a review.')
            return redirect('doctor_detail', id=id)
        
        # Check if already reviewed
        if Review.objects.filter(patient=patient, doctor=doctor).exists():
            messages.error(request, 'You have already reviewed this doctor.')
            return redirect('doctor_detail', id=id)
        
        # Get form data
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        if not rating:
            messages.error(request, 'Please select a rating.')
            return redirect('doctor_detail', id=id)
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Invalid rating value.')
            return redirect('doctor_detail', id=id)
        
        # Create review
        Review.objects.create(
            patient=patient,
            doctor=doctor,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, 'Thank you for your review!')
        
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('doctor_detail', id=id)

@login_required(login_url='login')
def book_appointment(request, id):
    # Check if user is a patient
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('doctors')
    
    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('doctors')
    
    slots = doctor.time_slots.all()
    return render(request, 'book_appointment.html', {'doctor': doctor, 'slots': slots})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password.')    
    return render(request, 'login.html')

def  signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    phone=phone,
                    user_type=user_type,
                )
                if user_type == 'patient':
                    Patient.objects.create(user=user)
                elif user_type == 'doctor':
                    Doctor.objects.create(user=user)
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Signup failed: {e}')
    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def google_login(request):
    """Initiate Google OAuth flow"""
    user_type = request.GET.get('type', 'patient')  # Get user type from URL parameter
    
    # Generate random state for security and store user type
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    request.session['oauth_user_type'] = user_type  # Store user type for callback
    
    # Build Google OAuth URL
    google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"{google_auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)

def google_callback(request):
    """Handle Google OAuth callback"""
    # Verify state to prevent CSRF
    state = request.GET.get('state')
    stored_state = request.session.get('oauth_state')
    
    if not state or state != stored_state:
        messages.error(request, 'Invalid state parameter. Please try again.')
        return redirect('login')
    
    # Get authorization code
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Authorization failed. Please try again.')
        return redirect('login')
    
    # Get stored user type
    user_type = request.session.get('oauth_user_type', 'patient')
    
    try:
        # Exchange code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()
        
        # Get user info from Google
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f"Bearer {tokens['access_token']}"}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_response.raise_for_status()
        user_data = userinfo_response.json()
        
        # Get or create user
        email = user_data.get('email')
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')
        picture_url = user_data.get('picture', '')
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'user_type': user_type,
            }
        )
        
        # For new users, create Doctor or Patient profile
        if created:
            with transaction.atomic():
                if user_type == 'doctor':
                    Doctor.objects.create(user=user)
                    messages.success(request, 'Doctor account created successfully! Welcome to MediConnect.')
                else:
                    Patient.objects.create(user=user)
                    messages.success(request, 'Patient account created successfully! Welcome to MediConnect.')
                
                # Download and save profile picture
                if picture_url:
                    try:
                        import urllib.request
                        from django.core.files.base import ContentFile
                        
                        img_data = urllib.request.urlopen(picture_url).read()
                        filename = f'google_{user.id}.jpg'
                        user.profile_image.save(filename, ContentFile(img_data), save=True)
                    except:
                        pass
        
        # Log the user in
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        if not created:
            messages.success(request, f'Welcome back, {user.first_name}!')
        
        # Clear oauth session data
        if 'oauth_state' in request.session:
            del request.session['oauth_state']
        if 'oauth_user_type' in request.session:
            del request.session['oauth_user_type']
        
        # Redirect based on user type
        if user.user_type == 'doctor':
            return redirect('dashboard')
        else:
            return redirect('index')
        
    except requests.RequestException as e:
        messages.error(request, f'Authentication failed: {str(e)}')
        return redirect('login')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('login')


@login_required(login_url='login')
def doctor_dashboard(request):
    
    # Ensure user is a doctor
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied. Doctors only.')
        return redirect('index')
    
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('index')
    
    # Get today's date and calculate date ranges
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday of current week
    week_end = week_start + timedelta(days=6)  # Sunday of current week
    
    # Total appointments (all time)
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    
    # Today's appointments
    todays_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today
    ).order_by('time_slot')
    todays_count = todays_appointments.count()
    
    # This week's appointments
    week_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=week_start,
        appointment_date__lte=week_end
    ).count()
    
    # Average rating and review count
    review_stats = Review.objects.filter(doctor=doctor).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )
    avg_rating = review_stats['avg_rating'] or 0.0
    review_count = review_stats['review_count']
    
    # Week overview (appointments per day)
    week_overview = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in range(7):
        day_date = week_start + timedelta(days=i)
        day_count = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=day_date
        ).count()
        week_overview.append({
            'day': days[i],
            'date': day_date,
            'count': day_count,
            'is_today': day_date == today
        })
    
    context = {
        'doctor': doctor,
        'total_appointments': total_appointments,
        'todays_count': todays_count,
        'week_appointments': week_appointments,
        'avg_rating': round(avg_rating, 1),
        'review_count': review_count,
        'todays_appointments': todays_appointments,
        'week_overview': week_overview,
        'today': today,
    }
    
    return render(request, 'doctor_dashboard.html', context)



# =========================
# API Views
# =========================

@api_view(['POST'])
def api_book_appointment(request, id):
    if not request.user.is_authenticated or request.user.user_type != 'patient':
        return Response({'error': 'Unauthorized. Only patients can book appointments.'}, status=403)
    
    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found.'}, status=404)
    
    appointment_date = request.data.get('appointment_date')
    time_slot = request.data.get('time_slot')
    reason = request.data.get('reason')
    
    if not (appointment_date and time_slot and reason):
        return Response({'error': 'Please fill all required fields'}, status=400)
    
    try:
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=request.user.patient,
            appointment_date=appointment_date,
            time_slot=time_slot,
            consultation_fee=doctor.consultation_fee,
            reason=reason,
            status='pending'
        )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PATCH'])
def api_confirm_appointment(request, id):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return Response({'error': 'Unauthorized. Only doctors can confirm appointments.'}, status=403)
    
    try:
        appointment = Appointment.objects.get(id=id, doctor=request.user.doctor)
        appointment.status = 'confirmed'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=200)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=404)

@api_view(['PATCH'])
def api_decline_appointment(request, id):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return Response({'error': 'Unauthorized. Only doctors can decline appointments.'}, status=403)
    
    try:
        appointment = Appointment.objects.get(id=id, doctor=request.user.doctor)
        appointment.status = 'declined'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=200)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=404)

@api_view(['PATCH'])
def api_cancel_appointment(request, id):
    if not request.user.is_authenticated:
        return Response({'error': 'Unauthorized'}, status=401)
    
    try:
        if request.user.user_type == 'patient':
            appointment = Appointment.objects.get(id=id, patient=request.user.patient)
        elif request.user.user_type == 'doctor':
            appointment = Appointment.objects.get(id=id, doctor=request.user.doctor)
        else:
            return Response({'error': 'Invalid user type.'}, status=400)
        
        appointment.status = 'cancelled'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=200)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=404)

@api_view(['GET'])
def api_time_slots_list(request):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return Response({'error': 'Unauthorized'}, status=403)
    
    slots = TimeSlot.objects.filter(doctor=request.user.doctor)
    serializer = TimeSlotSerializer(slots, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def api_add_slot(request):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return Response({'error': 'Unauthorized. Only doctors can add slots.'}, status=403)
    
    serializer = TimeSlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(doctor=request.user.doctor)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def api_del_slot(request, id):
    if not request.user.is_authenticated or request.user.user_type != 'doctor':
        return Response({'error': 'Unauthorized. Only doctors can delete slots.'}, status=403)
    
    try:
        slot = TimeSlot.objects.get(id=id, doctor=request.user.doctor)
        slot.delete()
        return Response({'message': 'Time slot deleted successfully.'}, status=200)
    except TimeSlot.DoesNotExist:
        return Response({'error': 'Time slot not found.'}, status=404)
