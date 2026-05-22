from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# =========================
# User Model
# =========================


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
    )
    
    phone = models.CharField(max_length=15 , blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    profile_image = models.FileField(upload_to='profile_images/', blank=True, null=True)
    username = None  # Removes username field
    
    objects = UserManager()

    # login configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name' , 'last_name']

    def __str__(self): 
        return f"{self.email} ({self.get_user_type_display()})"

# =========================
# Patient Model
# =========================

class Patient(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    user = models.OneToOneField(
    User, 
    on_delete=models.CASCADE,
    related_name='patient', 
    limit_choices_to={'user_type': 'patient'}
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True , choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5,blank=True)
    height = models.CharField(max_length=10,blank=True)
    weight = models.CharField(max_length=10,blank=True)
    address = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=200,blank=True)
    current_medication = models.CharField(max_length=200,blank=True)
    emergency_contact = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# =========================
# Specialization Model
# =========================

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='specializations/', blank=True, null=True)

    def __str__(self):
        return self.name

# =========================
# Doctor Model
# =========================

class Doctor(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='doctor',
    limit_choices_to={'user_type': 'doctor'}
    )
    license_number = models.CharField(max_length=20,blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    clinic_name = models.CharField(max_length=100, blank=True)
    clinic_address = models.CharField(max_length=255, blank=True)
    specialization = models.ForeignKey(Specialization, blank=True, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# =========================
# TimeSlot Model
# =========================
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} ({self.start_time} - {self.end_time})"

# =========================
# Appointment Model
# =========================
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('declined', 'Declined'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    consultation_fee = models.CharField(max_length=10)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.first_name + self.patient.user.last_name} → {self.doctor.user.first_name + ' ' + self.doctor.user.last_name} on {self.appointment_date}"

# =========================
# Review Model
# =========================
class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='review')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.patient.user.first_name} {self.patient.user.last_name}"

# =========================
# Contact Model
# =========================
class Contact(models.Model):
    SUBJECT_CHOICES = (
        ('General Inquiry', 'General Inquiry'),
        ('Technical Support', 'Technical Support'),
        ('Appointment Help', 'Appointment Help'),
        ('Billing Question', 'Billing Question'),
        ('Partnership Opportunity', 'Partnership Opportunity'),
        ('Other', 'Other'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=50,choices=SUBJECT_CHOICES)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Contact by {self.first_name + self.last_name}"
