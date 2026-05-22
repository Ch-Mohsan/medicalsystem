from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
	User,
	Patient,
	Doctor,
	Specialization,
	TimeSlot,
	Appointment,
	Review,
	Contact
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "email", "user_type", "is_staff", "date_joined")
	search_fields = ("first_name", "last_name", "email", "phone")
	list_filter = ("user_type", "is_staff", "is_active", "date_joined")
	ordering = ("-date_joined",)
	fieldsets = (
		("Personal Info", {"fields": ("first_name", "last_name", "phone", "profile_image")}),
		("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		("Important Dates", {"fields": ("last_login", "date_joined")}),
		("User Type", {"fields": ("user_type",)}),
	)
	add_fieldsets = (
		(None,{
			'fields': ('email', 'first_name', 'last_name', 'phone', 'user_type', 'password1', 'password2'),
		})
	)	

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ("user", "date_of_birth", "address", "emergency_contact")
	search_fields = ("user__first_name", "user__last_name", "address", "emergency_contact", "user__email")
	autocomplete_fields = ("user",)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
	list_display = ("user", "specialization", "qualification", "experience_years", "consultation_fee")
	search_fields = ("user__first_name", "user__last_name", "user__email", "specialization__name", "qualification")

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
	list_display = ("name",)
	search_fields = ("name",)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
	list_display = ("doctor", "start_time", "end_time")
	autocomplete_fields = ("doctor",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("patient", "doctor", "appointment_date", "time_slot", "status", "created_at")
	list_filter = ("status", "appointment_date")
	search_fields = ("patient__user__full_name", "doctor__user__full_name")
	autocomplete_fields = ("patient", "doctor")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','email','phone')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("patient", "doctor", "rating")
	search_fields = ("patient__user__full_name", "doctor__user__full_name")