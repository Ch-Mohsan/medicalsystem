# MediConnect - Healthcare Appointment System

A comprehensive Django-based web application for managing medical appointments between patients and doctors. MediConnect streamlines the appointment booking process, allowing patients to find doctors by specialization, read reviews, and book consultations online.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16.1-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Models](#database-models)
- [User Roles](#user-roles)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Sample Data](#sample-data)
- [Contributing](#contributing)

## ✨ Features

### For Patients
- 🔍 **Search & Filter**: Find doctors by name, specialization, experience, rating, and consultation fee
- 📅 **Book Appointments**: Select available time slots and book appointments instantly
- ⭐ **Review System**: Rate and review doctors after consultations
- 👤 **Profile Management**: Manage personal information, medical history, and emergency contacts
- 📊 **Appointment History**: View all past and upcoming appointments
- 🔔 **Real-time Status**: Track appointment status (Pending, Confirmed, Cancelled, Declined)

### For Doctors
- 📋 **Dashboard**: Comprehensive overview of appointments with statistics
- ⏰ **Time Slot Management**: Create and manage available consultation time slots
- 👥 **Patient Management**: View patient details and medical history
- ✅ **Appointment Management**: Confirm, decline, or manage appointment requests
- 📈 **Analytics**: View appointment trends and patient statistics
- 💼 **Profile Management**: Update qualifications, specialization, consultation fees, and clinic details

### Common Features
- 🔐 **Secure Authentication**: Email-based login system with custom user model
- 🔗 **Google OAuth Integration**: Optional sign-in with Google
- 📱 **Responsive Design**: Mobile-friendly interface with modern UI
- 🎨 **Tailwind CSS**: Professional and clean design
- 🔄 **RESTful API**: Backend APIs for dynamic operations
- 📧 **Contact System**: Built-in contact form for inquiries

## 🛠 Tech Stack

### Backend
- **Django 6.0.2** - Web framework
- **Django REST Framework 3.16.1** - API development
- **SQLite** - Database (development)
- **Python 3.9+** - Programming language

### Frontend
- **HTML5** - Markup
- **Tailwind CSS** - Styling
- **JavaScript** - Interactivity
- **Django Templates** - Template engine

### Additional Libraries
- **Pillow** - Image processing
- **python-dotenv** - Environment variable management
- **Requests** - HTTP library for OAuth
- **django-cors-headers** - CORS handling

## 📁 Project Structure

```
AppointmentSystem/
├── manage.py                          # Django management script
├── myproject/                         # Main project folder
│   ├── db.sqlite3                     # SQLite database
│   └── myproject/
│       ├── __init__.py
│       ├── settings.py                # Project settings
│       ├── urls.py                    # Root URL configuration
│       ├── wsgi.py                    # WSGI configuration
│       └── asgi.py                    # ASGI configuration
├── Mediconnect/                       # Main application
│   ├── __init__.py
│   ├── admin.py                       # Admin panel configuration
│   ├── apps.py                        # App configuration
│   ├── forms.py                       # Django forms
│   ├── models.py                      # Database models
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # View functions
│   ├── urls.py                        # App URL routing
│   ├── tests.py                       # Unit tests
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py       # Sample data generator
│   ├── migrations/                    # Database migrations
│   ├── static/
│   │   ├── CSS/
│   │   │   └── style.css              # Custom styles
│   │   ├── Images/                    # Static images
│   │   └── Js/
│   │       └── script.js              # JavaScript functionality
│   └── templates/                     # HTML templates
│       ├── base.html                  # Base template
│       ├── index.html                 # Home page
│       ├── doctors.html               # Doctor listing
│       ├── doctor_detail.html         # Doctor profile
│       ├── doctor_dashboard.html      # Doctor dashboard
│       ├── doctor_appointments.html   # Doctor appointments view
│       ├── patient_appointments.html  # Patient appointments view
│       ├── book_appointment.html      # Appointment booking
│       ├── profile.html               # User profiles
│       ├── login.html                 # Login page
│       ├── signup.html                # Registration page
│       ├── contact.html               # Contact form
│       └── about.html                 # About page
├── myvenv/                            # Virtual environment
├── profile_images/                    # User profile pictures
└── specializations/                   # Specialization icons
```

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AppointmentSystem
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv myvenv
myvenv\Scripts\activate

# Linux/Mac
python3 -m venv myvenv
source myvenv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django==6.0.2
pip install djangorestframework==3.16.1
pip install pillow==12.1.1
pip install python-dotenv==1.2.1
pip install requests==2.32.5
```

Or create a `requirements.txt` with the above packages and run:
```bash
pip install -r requirements.txt
```

### Step 4: Navigate to Project Directory
```bash
cd myproject
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 7: Populate Sample Data (Optional)
```bash
python manage.py populate_data
```

This command creates:
- 10 sample patients
- 10 sample doctors with different specializations
- 10 medical specializations
- 80 time slots (8 per doctor)
- 12 appointments with various statuses
- 10 reviews
- 5 contact form submissions

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root for sensitive configurations:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback/
```

### Settings Configuration

Key settings in `settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'Mediconnect.User'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = 'static/'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'
```

## 🗃️ Database Models

### User Model
Custom user model extending Django's AbstractUser with email-based authentication.

**Fields:**
- `email` - Unique email (used for login)
- `first_name`, `last_name` - User name
- `phone` - Contact number
- `user_type` - Role: patient, doctor, or admin
- `profile_image` - Profile picture

### Patient Model
Extended profile for patients linked to User model.

**Fields:**
- `user` - OneToOne relation with User
- `date_of_birth` - Birth date
- `gender` - Gender (Male, Female, Other, Prefer not to say)
- `blood_group` - Blood type
- `height`, `weight` - Physical measurements
- `address` - Residential address
- `allergies` - Known allergies
- `current_medication` - Current medications
- `emergency_contact` - Emergency contact information

### Doctor Model
Extended profile for doctors linked to User model.

**Fields:**
- `user` - OneToOne relation with User
- `license_number` - Medical license number
- `qualification` - Medical degree/qualifications
- `experience_years` - Years of practice
- `consultation_fee` - Consultation charges
- `specialization` - ForeignKey to Specialization
- `clinic_name` - Hospital/clinic name
- `clinic_address` - Practice location
- `bio` - Professional biography
- `rating` - Average rating (calculated from reviews)

### Specialization Model
Medical specializations for categorizing doctors.

**Fields:**
- `name` - Specialization name (e.g., Cardiology, Dermatology)
- `description` - Detailed description
- `icon` - Specialization icon/image

### TimeSlot Model
Available consultation time slots for doctors.

**Fields:**
- `doctor` - ForeignKey to Doctor
- `start_time` - Slot start time
- `end_time` - Slot end time

### Appointment Model
Appointment bookings between patients and doctors.

**Fields:**
- `patient` - ForeignKey to Patient
- `doctor` - ForeignKey to Doctor
- `appointment_date` - Date of appointment
- `time_slot` - Selected time slot
- `status` - Status (pending, confirmed, cancelled, declined)
- `consultation_fee` - Fee for the appointment
- `reason` - Reason for consultation
- `created_at` - Booking timestamp

### Review Model
Patient reviews and ratings for doctors.

**Fields:**
- `patient` - ForeignKey to Patient
- `doctor` - ForeignKey to Doctor
- `rating` - Rating (1-5)
- `comment` - Review text
- `created_at` - Review timestamp

### Contact Model
Contact form submissions.

**Fields:**
- `first_name`, `last_name` - Contact name
- `email` - Contact email
- `phone` - Contact phone
- `subject` - Inquiry subject
- `message` - Inquiry message

## 👥 User Roles

### Patient
- Browse and search doctors
- View doctor profiles and reviews
- Book appointments
- Manage appointments (view, cancel)
- Submit reviews
- Update profile and medical information

### Doctor
- View personalized dashboard with statistics
- Manage time slots
- View and manage appointment requests
- Confirm or decline appointments
- View patient information
- Update professional profile

### Admin
- Full access to Django admin panel
- Manage users, doctors, patients
- Manage specializations
- View all appointments and reviews
- System configuration

### Sample Login Credentials (After populate_data)

**Patient:**
- Email: `ahmed.khan@gmail.com`
- Password: `patient123`

**Doctor:**
- Email: `dr.asim.malik@gmail.com`
- Password: `doctor123`

## 🔌 API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /signup/` - User registration
- `POST /logout/` - User logout
- `GET /auth/google/` - Google OAuth login
- `GET /auth/google/callback/` - Google OAuth callback

### Public Views
- `GET /` - Home page
- `GET /doctors/` - Doctor listing with filters
- `GET /doctor/<int:id>/` - Doctor detail page
- `GET /about/` - About page
- `POST /contact/` - Contact form submission

### Patient APIs
- `POST /api/appointment/book/<int:id>/` - Book appointment
- `POST /api/appointment/cancel/<int:id>/` - Cancel appointment
- `POST /doctor/<int:id>/review/` - Add review

### Doctor APIs
- `GET /api/slots/` - Get doctor's time slots
- `POST /api/slots/add/` - Add new time slot
- `DELETE /api/slots/del/<int:id>/` - Delete time slot
- `POST /api/appointment/confirm/<int:id>/` - Confirm appointment
- `POST /api/appointment/decline/<int:id>/` - Decline appointment

### User Profile
- `GET /profile/` - View/edit user profile
- `GET /appointments/` - View appointments
- `GET /dashboard/` - Doctor dashboard

## 📖 Usage

### For Patients

1. **Register/Login**
   - Sign up with email and password
   - Or login with existing credentials
   - Optional Google OAuth sign-in

2. **Find a Doctor**
   - Browse doctors on the home page
   - Use search and filter options:
     - Search by name
     - Filter by specialization
     - Filter by experience, rating, or consultation fee
     - Sort results

3. **Book Appointment**
   - Click on a doctor's profile
   - Select date and available time slot
   - Provide reason for consultation
   - Submit booking request

4. **Manage Appointments**
   - View all appointments in "My Appointments"
   - Check appointment status
   - Cancel appointments if needed

5. **Write Reviews**
   - After consultation, rate the doctor (1-5 stars)
   - Write a review about your experience

### For Doctors

1. **Complete Profile**
   - Add license number, qualifications
   - Set specialization and consultation fee
   - Update clinic information
   - Add professional bio

2. **Set Availability**
   - Add time slots from dashboard
   - Create multiple slots for different days
   - Delete unavailable slots

3. **Manage Appointments**
   - View appointment requests on dashboard
   - Check patient details before confirming
   - Confirm or decline appointment requests
   - View appointment history

4. **Dashboard Analytics**
   - View total appointments
   - See pending requests
   - Track confirmed appointments
   - Monitor monthly statistics

## 📊 Sample Data

The `populate_data` management command creates realistic sample data:

### Users Created
- **10 Patients**: Pakistani names with realistic contact info
- **10 Doctors**: Various specializations with complete profiles

### Specializations
- Cardiology
- Dermatology
- Pediatrics
- Orthopedics
- Neurology
- Ophthalmology
- Psychiatry
- General Surgery
- ENT Specialist
- Gynecology

### Sample Doctors
1. Dr. Asim Malik - Cardiologist (15 years experience)
2. Dr. Sarah Ahmed - Dermatologist (12 years experience)
3. Dr. Kamran Shah - Pediatrician (8 years experience)
4. Dr. Nadia Khan - Orthopedic Surgeon (20 years experience)
5. Dr. Tariq Mehmood - Neurologist (18 years experience)
... and more

### Appointments & Reviews
- Multiple appointments with different statuses
- Reviews with ratings and comments
- Contact form submissions

## 🎨 Frontend Features

### Modern UI/UX
- Clean and professional design
- Responsive layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Interactive elements
- Form validation
- Toast notifications

### Components
- Navigation bar with user menu
- Search and filter forms
- Doctor cards with ratings
- Appointment booking modal
- Profile edit forms
- Dashboard charts and statistics

## 🧪 Testing

Run tests with:
```bash
python manage.py test Mediconnect
```

## 📝 Development

### Adding a New Specialization
1. Go to Admin Panel: `http://127.0.0.1:8000/admin/`
2. Navigate to Specializations
3. Click "Add Specialization"
4. Fill in name, description, and upload icon
5. Save

### Customizing Email Templates
Edit email configurations in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up PostgreSQL/MySQL database
- [ ] Configure static files with WhiteNoise or CDN
- [ ] Set up media file storage (AWS S3, etc.)
- [ ] Enable HTTPS
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Run security check: `python manage.py check --deploy`

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: VPS with Ubuntu + Nginx + Gunicorn
- **Railway**: Simple deployment for Django apps
- **PythonAnywhere**: Beginner-friendly hosting
- **AWS**: Scalable production environment

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/YourFeature`)
6. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation as needed
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Developed with ❤️ by [Your Name]

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Tailwind CSS
- All contributors and users

## 📧 Contact & Support

- **Email**: contact@mediconnect.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/mediconnect/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/mediconnect/wiki)

---

**Note**: This is a demonstration project. For production use, implement additional security measures, comprehensive testing, and proper deployment configurations.

## 🔮 Future Enhancements

- [ ] Email notifications for appointments
- [ ] SMS reminders
- [ ] Video consultation integration
- [ ] Payment gateway integration
- [ ] Medical records management
- [ ] Prescription management
- [ ] Multi-language support
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics for doctors
- [ ] Insurance integration
- [ ] Telemedicine features
- [ ] Chat functionality

---

**Last Updated**: February 2026
