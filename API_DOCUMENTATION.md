# MediConnect API Documentation

Complete API reference for the MediConnect Healthcare Appointment System.

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Public Endpoints](#public-endpoints)
3. [Patient Endpoints](#patient-endpoints)
4. [Doctor Endpoints](#doctor-endpoints)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)

## 🔐 Authentication

MediConnect uses session-based authentication with Django's built-in authentication system.

### Login Required

Most endpoints require authentication. Unauthenticated requests will redirect to the login page or return a 401 Unauthorized response for API endpoints.

### Session Authentication

After successful login, a session cookie is set and used for subsequent requests.

---

## 🌐 Public Endpoints

### 1. Home Page

```
GET /
```

**Description**: Landing page with top-rated doctors and search functionality

**Response**: HTML page

**Features**:
- Top 3 rated doctors
- All specializations for search
- Search form for finding doctors

---

### 2. Doctor Listing

```
GET /doctors/
```

**Description**: Browse and search doctors with advanced filters

**Query Parameters**:
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `name` | string | Search by doctor name | `?name=Asim` |
| `specialization` | string | Filter by specialization | `?specialization=Cardiology` |
| `min_rating` | float | Minimum rating (1-5) | `?min_rating=4.0` |
| `fee` | string | Fee range filter | `?fee=under_5000` |
| `experience` | string | Experience range | `?experience=10_plus` |
| `sort_by` | string | Sort order | `?sort_by=rating_high` |

**Fee Range Options**:
- `under_5000`: Less than Rs. 5,000
- `5000_10000`: Rs. 5,000 - 10,000
- `10000_15000`: Rs. 10,000 - 15,000
- `15000_plus`: More than Rs. 15,000

**Experience Range Options**:
- `0_5`: 0-5 years
- `5_10`: 5-10 years
- `10_plus`: More than 10 years

**Sort By Options**:
- `rating_high`: Highest rating first
- `rating_low`: Lowest rating first
- `experience_high`: Most experienced first
- `experience_low`: Least experienced first
- `fee_low`: Lowest fee first
- `fee_high`: Highest fee first

**Example Request**:
```
GET /doctors/?specialization=Cardiology&min_rating=4.0&sort_by=rating_high
```

**Response**: HTML page with filtered doctors

---

### 3. Doctor Detail

```
GET /doctor/<int:id>/
```

**Description**: View detailed doctor profile with reviews

**URL Parameters**:
- `id` (integer, required): Doctor ID

**Response**: HTML page with:
- Doctor information (qualifications, experience, etc.)
- All reviews with ratings
- Available time slots
- Book appointment button

**Example**:
```
GET /doctor/1/
```

---

### 4. About Page

```
GET /about/
```

**Description**: Information about the platform

**Response**: HTML page

---

### 5. Contact Form

```
GET /contact/
POST /contact/
```

**Description**: Contact form submission

**POST Body**:
```json
{
    "first_name": "Ahmed",
    "last_name": "Khan",
    "email": "ahmed@example.com",
    "phone": "0300-1234567",
    "subject": "General Inquiry",
    "message": "I have a question about..."
}
```

**Subject Options**:
- General Inquiry
- Technical Support
- Appointment Help
- Billing Question
- Partnership Opportunity
- Other

**Response**:
- Success: Redirect with success message
- Error: Form with validation errors

---

## 🔒 Authentication Endpoints

### 1. Login

```
POST /login/
```

**Description**: User authentication

**POST Body**:
```json
{
    "email": "ahmed.khan@gmail.com",
    "password": "patient123"
}
```

**Success Response**:
- Status: 302 Redirect
- Redirects to: Homepage or dashboard (based on user type)

**Error Response**:
- Returns login page with error message

---

### 2. Signup

```
POST /signup/
```

**Description**: New user registration

**POST Body**:
```json
{
    "first_name": "New",
    "last_name": "User",
    "email": "newuser@example.com",
    "phone": "0300-1234567",
    "password": "securepassword",
    "confirm_password": "securepassword",
    "user_type": "patient"
}
```

**User Types**:
- `patient`: Patient account
- `doctor`: Doctor account

**Success Response**:
- Status: 302 Redirect
- Creates user and patient/doctor profile
- Redirects to login page

**Validation Rules**:
- Email must be unique
- Password confirmation must match
- All required fields must be filled

---

### 3. Logout

```
POST /logout/
```

**Description**: End user session

**Response**: Redirect to homepage

---

### 4. Google OAuth Login

```
GET /auth/google/
```

**Description**: Initiate Google OAuth flow

**Response**: Redirect to Google login page

---

### 5. Google OAuth Callback

```
GET /auth/google/callback/
```

**Description**: Handle Google OAuth callback

**Query Parameters**:
- `code`: Authorization code from Google

**Response**: 
- Success: Create/login user, redirect to homepage
- Error: Redirect to login with error message

---

## 👤 Patient Endpoints

### 1. View Profile

```
GET /profile/
```

**Authentication**: Required (Patient)

**Description**: View and edit patient profile

**Response**: HTML page with user and patient forms

---

### 2. Update Profile

```
POST /profile/
```

**Authentication**: Required (Patient)

**POST Body** (multipart/form-data):
```json
{
    "first_name": "Ahmed",
    "last_name": "Khan",
    "email": "ahmed@example.com",
    "phone": "0300-1234567",
    "profile_image": "<file>",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "blood_group": "A+",
    "height": "175",
    "weight": "70",
    "address": "House 123, Street 45, Karachi",
    "allergies": "None",
    "current_medication": "None",
    "emergency_contact": "0321-9876543"
}
```

**Response**: Redirect to profile with success/error message

---

### 3. View Appointments

```
GET /appointments/
```

**Authentication**: Required (Patient)

**Description**: List all patient appointments

**Response**: HTML page with appointments ordered by date (newest first)

**Appointment Information**:
- Doctor details
- Appointment date and time
- Status (pending, confirmed, cancelled, declined)
- Consultation fee
- Reason for visit

---

### 4. Book Appointment

```
GET /book-appointment/<int:id>/
```

**Authentication**: Required (Patient)

**URL Parameters**:
- `id` (integer, required): Doctor ID

**Description**: View appointment booking form

**Response**: HTML page with:
- Doctor information
- Available time slots
- Booking form

---

### 5. Book Appointment (API)

```
POST /api/appointment/book/<int:id>/
```

**Authentication**: Required (Patient)

**URL Parameters**:
- `id` (integer, required): Doctor ID

**POST Body**:
```json
{
    "appointment_date": "2026-03-15",
    "time_slot": "09:00 AM - 10:00 AM",
    "reason": "Regular checkup"
}
```

**Success Response**:
```json
{
    "success": true,
    "message": "Appointment booked successfully",
    "appointment_id": 123
}
```

**Error Response**:
```json
{
    "success": false,
    "message": "Time slot not available"
}
```

---

### 6. Cancel Appointment (API)

```
POST /api/appointment/cancel/<int:id>/
```

**Authentication**: Required (Patient)

**URL Parameters**:
- `id` (integer, required): Appointment ID

**Success Response**:
```json
{
    "success": true,
    "message": "Appointment cancelled successfully"
}
```

**Error Response**:
```json
{
    "success": false,
    "message": "Cannot cancel this appointment"
}
```

---

### 7. Add Review

```
POST /doctor/<int:id>/review/
```

**Authentication**: Required (Patient)

**URL Parameters**:
- `id` (integer, required): Doctor ID

**POST Body**:
```json
{
    "rating": 5,
    "comment": "Excellent doctor, very professional and caring."
}
```

**Validation**:
- Rating: 1-5 (integer)
- Comment: Optional text

**Response**: Redirect to doctor detail page with success message

---

## 👨‍⚕️ Doctor Endpoints

### 1. Doctor Dashboard

```
GET /dashboard/
```

**Authentication**: Required (Doctor)

**Description**: Doctor's main dashboard with statistics and appointments

**Response**: HTML page with:
- Total appointments count
- Pending appointments count
- Confirmed appointments count
- Monthly statistics
- Recent appointments
- Time slot management

---

### 2. View Profile

```
GET /profile/
```

**Authentication**: Required (Doctor)

**Description**: View and edit doctor profile

**Response**: HTML page with user and doctor forms

---

### 3. Update Profile

```
POST /profile/
```

**Authentication**: Required (Doctor)

**POST Body** (multipart/form-data):
```json
{
    "first_name": "Dr. Asim",
    "last_name": "Malik",
    "email": "dr.asim@example.com",
    "phone": "0300-1111111",
    "profile_image": "<file>",
    "license_number": "PMC-12345",
    "qualification": "MBBS, FCPS (Cardiology)",
    "experience_years": 15,
    "consultation_fee": 5000,
    "specialization": 1,
    "clinic_name": "City Hospital",
    "clinic_address": "Main Boulevard, Karachi",
    "bio": "Experienced cardiologist..."
}
```

**Response**: Redirect to profile with success/error message

---

### 4. View Appointments

```
GET /appointments/
```

**Authentication**: Required (Doctor)

**Description**: List all doctor appointments

**Response**: HTML page with appointments grouped by status

---

### 5. View Patient Details

```
GET /patient/<int:id>/
```

**Authentication**: Required (Doctor)

**URL Parameters**:
- `id` (integer, required): Patient ID

**Description**: View patient profile and medical information

**Response**: HTML page with:
- Patient demographics
- Medical information
- Emergency contact
- Appointment history

---

### 6. Get Time Slots (API)

```
GET /api/slots/
```

**Authentication**: Required (Doctor)

**Description**: Retrieve doctor's time slots

**Success Response**:
```json
[
    {
        "id": 1,
        "doctor": 5,
        "start_time": "09:00:00",
        "end_time": "10:00:00"
    },
    {
        "id": 2,
        "doctor": 5,
        "start_time": "10:00:00",
        "end_time": "11:00:00"
    }
]
```

---

### 7. Add Time Slot (API)

```
POST /api/slots/add/
```

**Authentication**: Required (Doctor)

**POST Body**:
```json
{
    "start_time": "14:00",
    "end_time": "15:00"
}
```

**Success Response**:
```json
{
    "success": true,
    "message": "Time slot added successfully",
    "slot": {
        "id": 15,
        "start_time": "14:00:00",
        "end_time": "15:00:00"
    }
}
```

**Error Response**:
```json
{
    "success": false,
    "errors": {
        "start_time": ["This field is required"]
    }
}
```

---

### 8. Delete Time Slot (API)

```
DELETE /api/slots/del/<int:id>/
```

**Authentication**: Required (Doctor)

**URL Parameters**:
- `id` (integer, required): Time slot ID

**Success Response**:
```json
{
    "success": true,
    "message": "Time slot deleted successfully"
}
```

**Error Response**:
```json
{
    "success": false,
    "message": "Time slot not found"
}
```

---

### 9. Confirm Appointment (API)

```
POST /api/appointment/confirm/<int:id>/
```

**Authentication**: Required (Doctor)

**URL Parameters**:
- `id` (integer, required): Appointment ID

**Success Response**:
```json
{
    "success": true,
    "message": "Appointment confirmed successfully"
}
```

**Error Response**:
```json
{
    "success": false,
    "message": "Appointment not found"
}
```

---

### 10. Decline Appointment (API)

```
POST /api/appointment/decline/<int:id>/
```

**Authentication**: Required (Doctor)

**URL Parameters**:
- `id` (integer, required): Appointment ID

**Success Response**:
```json
{
    "success": true,
    "message": "Appointment declined"
}
```

---

## 📊 Response Formats

### Success Response (API)

```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Response data
    }
}
```

### Error Response (API)

```json
{
    "success": false,
    "message": "Error message",
    "errors": {
        "field_name": ["Error description"]
    }
}
```

### Appointment Object

```json
{
    "id": 123,
    "patient": {
        "id": 5,
        "user": {
            "email": "patient@example.com",
            "first_name": "Ahmed",
            "last_name": "Khan"
        }
    },
    "doctor": {
        "id": 3,
        "user": {
            "email": "doctor@example.com",
            "first_name": "Dr. Sarah",
            "last_name": "Ahmed"
        },
        "specialization": "Dermatology",
        "consultation_fee": "3000"
    },
    "appointment_date": "2026-03-15",
    "time_slot": "09:00 AM - 10:00 AM",
    "status": "pending",
    "reason": "Skin checkup",
    "created_at": "2026-02-24T10:30:00Z"
}
```

---

## ❌ Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `302 Found`: Redirect
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Common Error Messages

**Authentication Errors**:
```json
{
    "success": false,
    "message": "Please login to continue"
}
```

**Permission Errors**:
```json
{
    "success": false,
    "message": "You don't have permission to perform this action"
}
```

**Validation Errors**:
```json
{
    "success": false,
    "message": "Validation failed",
    "errors": {
        "email": ["This field is required"],
        "phone": ["Enter a valid phone number"]
    }
}
```

**Not Found Errors**:
```json
{
    "success": false,
    "message": "Doctor not found"
}
```

---

## 🔧 Testing APIs

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/login/ \
  -d "email=patient@example.com&password=patient123" \
  -c cookies.txt

# Book appointment (with session cookie)
curl -X POST http://localhost:8000/api/appointment/book/1/ \
  -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"appointment_date":"2026-03-15","time_slot":"09:00 AM - 10:00 AM","reason":"Checkup"}'
```

### Using Python Requests

```python
import requests

# Create session
session = requests.Session()

# Login
login_data = {
    'email': 'patient@example.com',
    'password': 'patient123'
}
session.post('http://localhost:8000/login/', data=login_data)

# Book appointment
appointment_data = {
    'appointment_date': '2026-03-15',
    'time_slot': '09:00 AM - 10:00 AM',
    'reason': 'Regular checkup'
}
response = session.post(
    'http://localhost:8000/api/appointment/book/1/',
    json=appointment_data
)
print(response.json())
```

---

## 📝 Notes

- All API endpoints return JSON responses
- Session authentication is required for protected endpoints
- CSRF token is required for POST requests from web forms
- Time format: 24-hour (HH:MM:SS) in database, displayed as 12-hour with AM/PM
- Date format: YYYY-MM-DD
- All timestamps are in UTC

---

For more information, see the [main README](README.md) or [contributing guidelines](CONTRIBUTING.md).
