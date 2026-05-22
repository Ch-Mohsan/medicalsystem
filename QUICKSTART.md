# Quick Start Guide - MediConnect

Get your MediConnect healthcare appointment system up and running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Python Requirements
```bash
# Navigate to project directory
cd AppointmentSystem

# Create virtual environment
python -m venv myvenv

# Activate virtual environment
# Windows:
myvenv\Scripts\activate
# Mac/Linux:
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Navigate to project folder
cd myproject

# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 3. Load Sample Data (Optional but Recommended)
```bash
python manage.py populate_data
```
This creates:
- 10 sample patients
- 10 sample doctors
- Various specializations
- Sample appointments and reviews

### 4. Run the Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 🔑 Test Login Credentials

After running `populate_data`:

**Patient Account:**
- Email: `ahmed.khan@gmail.com`
- Password: `patient123`

**Doctor Account:**
- Email: `dr.asim.malik@gmail.com`
- Password: `doctor123`

**Admin Panel:**
- Access: `http://127.0.0.1:8000/admin/`
- Use superuser credentials created in step 2

## 📱 What to Try

### As a Patient:
1. Browse doctors on homepage
2. Search/filter doctors by specialization
3. View doctor profiles and reviews
4. Book an appointment
5. Check "My Appointments"
6. Update your profile

### As a Doctor:
1. Login with doctor credentials
2. Complete your profile
3. Add time slots in dashboard
4. View pending appointments
5. Confirm/decline appointments
6. Check dashboard statistics

### As Admin:
1. Access admin panel
2. Manage users, doctors, patients
3. Add new specializations
4. View all appointments

## 🛠 Common Commands

```bash
# Create new admin user
python manage.py createsuperuser

# Make migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Clear and repopulate sample data
python manage.py populate_data
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8080
```

### Database Locked Error
```bash
# Stop all Django servers and try again
# Or delete db.sqlite3 and run migrations again
```

### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

### Static Files Not Loading
```bash
# Check DEBUG=True in settings.py
# Run collectstatic
python manage.py collectstatic --noinput
```

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize templates in `Mediconnect/templates/`
- Modify styles in `Mediconnect/static/CSS/style.css`
- Add new features in `Mediconnect/views.py`
- Configure Google OAuth (see .env.example)

## 💡 Tips

1. **Development**: Keep DEBUG=True for development
2. **Testing**: Use sample data to test all features
3. **Customization**: Start by modifying templates and CSS
4. **Database**: Backup db.sqlite3 before major changes
5. **Documentation**: Check inline comments in code

## 🆘 Need Help?

- Check the [full documentation](README.md)
- Review Django documentation: https://docs.djangoproject.com/
- Check the code comments for guidance
- Open an issue on GitHub

---

Happy coding! 🎉
