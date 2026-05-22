from django import forms
from .models import Contact, User, Doctor, Patient, Specialization

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'subject': 'Subject',
            'message': 'Message',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, 'placeholder': 'Tell us how we can help you...'}),
        }


# User Profile Forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'profile_image']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone',
            'email': 'Email',
            'profile_image': 'Profile Image',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'profile_image': forms.FileInput(attrs={'class': 'hidden', 'id': 'profileImageInput', 'accept': 'image/*'}),
        }


# Doctor Profile Form
class DoctorProfileForm(forms.ModelForm):
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        empty_label="Select Specialization",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    class Meta:
        model = Doctor
        fields = ['license_number', 'qualification', 'experience_years', 'consultation_fee', 
                  'specialization', 'clinic_name', 'clinic_address', 'bio']
        labels = {
            'license_number': 'License Number',
            'qualification': 'Medical Degree',
            'experience_years': 'Years of Experience',
            'consultation_fee': 'Consultation Fee',
            'specialization': 'Specialization',
            'clinic_name': 'Hospital/Clinic Name',
            'clinic_address': 'Address',
            'bio': 'About Me',
        }
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-input'}),
            'qualification': forms.TextInput(attrs={'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-input'}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-input'}),
            'clinic_address': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }


# Patient Profile Form
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'blood_group', 'height', 'weight', 
                  'address', 'allergies', 'current_medication', 'emergency_contact']
        labels = {
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'blood_group': 'Blood Group',
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'address': 'Address',
            'allergies': 'Allergies',
            'current_medication': 'Current Medications',
            'emergency_contact': 'Emergency Contact',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Blood Group'),
                ('A+', 'A+'), ('A-', 'A-'),
                ('B+', 'B+'), ('B-', 'B-'),
                ('AB+', 'AB+'), ('AB-', 'AB-'),
                ('O+', 'O+'), ('O-', 'O-'),
            ]),
            'height': forms.NumberInput(attrs={'class': 'form-input'}),
            'weight': forms.NumberInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'allergies': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'List any allergies...'
            }),
            'current_medication': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'List current medications...'
            }),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-input'}),
        }
