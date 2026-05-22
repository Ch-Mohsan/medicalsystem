from rest_framework import serializers
from .models import User, Doctor, Patient, Appointment, TimeSlot

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'phone']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'qualification', 'experience_years', 'consultation_fee', 'clinic_name', 'clinic_address']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'user', 'gender', 'date_of_birth', 'blood_group']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'end_time']
        read_only_fields = ['doctor']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_details', 'patient_details', 'appointment_date', 'time_slot', 'status', 'consultation_fee', 'reason', 'created_at']
        read_only_fields = ['patient', 'status', 'created_at', 'consultation_fee', 'doctor']
