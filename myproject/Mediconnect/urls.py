from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointments/', views.appointments, name='appointments'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor/<int:id>/review/', views.add_review, name='add_review'),
    path('patient/<int:id>/', views.patient_detail, name='patient_detail'),
    path('book-appointment/<int:id>/', views.book_appointment, name='book_appointment'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('auth/google/', views.google_login, name='google_login'),
    path('auth/google/callback/', views.google_callback, name='google_callback'),
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    
    # API Endpoints
    path('api/appointment/book/<int:id>/', views.api_book_appointment, name='api_book_appointment'),
    path('api/appointment/confirm/<int:id>/', views.api_confirm_appointment, name='api_confirm_appointment'),
    path('api/appointment/decline/<int:id>/', views.api_decline_appointment, name='api_decline_appointment'),
    path('api/appointment/cancel/<int:id>/', views.api_cancel_appointment, name='api_cancel_appointment'),
    path('api/slots/', views.api_time_slots_list, name='api_time_slots_list'),
    path('api/slots/add/', views.api_add_slot, name='api_add_slot'),
    path('api/slots/del/<int:id>/', views.api_del_slot, name='api_del_slot'),
]