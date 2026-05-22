# MediConnect Deployment Guide

Complete guide for deploying MediConnect to production environments.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Security Settings](#security-settings)
4. [Database Setup](#database-setup)
5. [Static Files](#static-files)
6. [Deployment Options](#deployment-options)
7. [Post-Deployment](#post-deployment)
8. [Monitoring](#monitoring)
9. [Backup Strategy](#backup-strategy)

## ✅ Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass (`python manage.py test`)
- [ ] Security check completed (`python manage.py check --deploy`)
- [ ] Debug mode is disabled
- [ ] Secret key is secure and not in version control
- [ ] Database credentials are secure
- [ ] Static files are collected
- [ ] Media files storage is configured
- [ ] HTTPS is enabled
- [ ] Email backend is configured
- [ ] Backup strategy is in place
- [ ] Monitoring tools are set up

## ⚙️ Environment Configuration

### 1. Create Production Environment File

Create `.env.production`:

```bash
# Django Core Settings
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended for production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=mediconnect_prod
DB_USER=mediconnect_user
DB_PASSWORD=strong-database-password
DB_HOST=localhost
DB_PORT=5432

# Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-app-password
DEFAULT_FROM_EMAIL=MediConnect <noreply@yourdomain.com>

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-production-google-client-id
GOOGLE_CLIENT_SECRET=your-production-google-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback/

# Storage (AWS S3 - Optional)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=mediconnect-prod
AWS_S3_REGION_NAME=us-east-1

# Sentry (Error Tracking - Optional)
SENTRY_DSN=your-sentry-dsn-here
```

### 2. Update settings.py for Production

Add to `settings.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security Settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# HTTPS/Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Database
if os.getenv('DB_ENGINE'):
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Static files (production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media files (production)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# AWS S3 (if using)
if os.getenv('USE_S3') == 'True':
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Sentry (Optional)
if os.getenv('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )
```

## 🔒 Security Settings

### 1. Generate Secure Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Security Checklist

```bash
# Run Django security check
python manage.py check --deploy
```

Fix all warnings before deploying.

### 3. CORS Configuration (if needed)

```bash
pip install django-cors-headers
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

## 🗄️ Database Setup

### PostgreSQL (Recommended)

#### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

#### 2. Create Database

```bash
sudo -u postgres psql

postgres=# CREATE DATABASE mediconnect_prod;
postgres=# CREATE USER mediconnect_user WITH PASSWORD 'strong-password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE mediconnect_prod TO mediconnect_user;
postgres=# \q
```

#### 3. Install Python Driver

```bash
pip install psycopg2-binary
```

#### 4. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### MySQL (Alternative)

```bash
# Install
sudo apt install mysql-server

# Create database
mysql -u root -p
mysql> CREATE DATABASE mediconnect_prod;
mysql> CREATE USER 'mediconnect_user'@'localhost' IDENTIFIED BY 'strong-password';
mysql> GRANT ALL PRIVILEGES ON mediconnect_prod.* TO 'mediconnect_user'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> quit

# Install driver
pip install mysqlclient
```

## 📁 Static Files

### 1. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2. Configure WhiteNoise (Alternative to S3)

```bash
pip install whitenoise
```

Add to `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🚀 Deployment Options

---

## Option 1: DigitalOcean (VPS)

### Step 1: Create Droplet

- Choose Ubuntu 22.04 LTS
- Select appropriate size (minimum 2GB RAM)
- Add SSH key

### Step 2: Server Setup

```bash
# Connect to server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Create user
adduser mediconnect
usermod -aG sudo mediconnect
su - mediconnect
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/mediconnect.git
cd mediconnect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Setup database
python myproject/manage.py migrate
python myproject/manage.py collectstatic
python myproject/manage.py createsuperuser
```

### Step 4: Configure Gunicorn

Create `/etc/systemd/system/mediconnect.service`:

```ini
[Unit]
Description=MediConnect Django Application
After=network.target

[Service]
User=mediconnect
Group=www-data
WorkingDirectory=/home/mediconnect/mediconnect/myproject
Environment="PATH=/home/mediconnect/mediconnect/venv/bin"
ExecStart=/home/mediconnect/mediconnect/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/mediconnect/mediconnect/myproject.sock \
    myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start mediconnect
sudo systemctl enable mediconnect
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/mediconnect`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/mediconnect/mediconnect/myproject/staticfiles/;
    }
    
    location /media/ {
        alias /home/mediconnect/mediconnect/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/mediconnect/mediconnect/myproject.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/mediconnect /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo systemctl restart nginx
```

---

## Option 2: Heroku

### Step 1: Prepare Application

Create `Procfile`:
```
web: gunicorn myproject.myproject.wsgi --log-file -
release: python myproject/manage.py migrate
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt`:
```bash
pip install gunicorn dj-database-url whitenoise
pip freeze > requirements.txt
```

### Step 2: Heroku Configuration

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'

# Deploy
git push heroku main

# Run migrations
heroku run python myproject/manage.py migrate
heroku run python myproject/manage.py createsuperuser
```

---

## Option 3: PythonAnywhere

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create a new web app (Django)
3. Clone repository in Bash console
4. Configure virtual environment
5. Set up WSGI file
6. Configure static files
7. Reload web app

---

## Option 4: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

---

## 🔍 Post-Deployment

### 1. Create Superuser

```bash
python manage.py createsuperuser
```

### 2. Test Application

- Visit homepage
- Test user registration
- Test login/logout
- Book test appointment
- Check admin panel

### 3. Load Initial Data (Optional)

```bash
python manage.py populate_data
```

### 4. Configure Domain

- Update DNS records
- Configure SSL certificate
- Update ALLOWED_HOSTS

## 📊 Monitoring

### 1. Error Tracking (Sentry)

```bash
pip install sentry-sdk
```

Configure in `settings.py` (see above)

### 2. Application Performance Monitoring

Consider tools like:
- New Relic
- DataDog
- Scout APM

### 3. Server Monitoring

```bash
# Install monitoring tools
sudo apt install htop

# Check logs
sudo journalctl -u mediconnect -f
sudo tail -f /var/log/nginx/error.log
```

### 4. Database Monitoring

```bash
# PostgreSQL
sudo -u postgres psql
postgres=# \l  # List databases
postgres=# \dt  # List tables
```

## 💾 Backup Strategy

### 1. Database Backup

```bash
# PostgreSQL
pg_dump mediconnect_prod > backup_$(date +%Y%m%d).sql

# Automated backup script
cat > /home/mediconnect/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/mediconnect/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump mediconnect_prod > $BACKUP_DIR/db_$DATE.sql
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
EOF

chmod +x /home/mediconnect/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /home/mediconnect/backup.sh
```

### 2. Media Files Backup

```bash
# Rsync media files
rsync -avz /home/mediconnect/mediconnect/media/ /backup/media/

# Or use tar
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### 3. Automated Backups to S3

```bash
pip install boto3

# Create backup script
python manage.py dumpdata > backup.json
# Upload to S3 using boto3
```

## 🔄 Updates and Maintenance

### Deploy Updates

```bash
# On server
cd /home/mediconnect/mediconnect
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python myproject/manage.py migrate
python myproject/manage.py collectstatic --noinput
sudo systemctl restart mediconnect
sudo systemctl restart nginx
```

### Rolling Back

```bash
# Revert to previous commit
git revert HEAD
# Or checkout specific version
git checkout v1.0.0

# Restore database backup if needed
psql mediconnect_prod < backup_YYYYMMDD.sql
```

## 📝 Troubleshooting

### 502 Bad Gateway
- Check Gunicorn status: `sudo systemctl status mediconnect`
- Check socket file permissions
- Review Nginx error logs

### Static Files Not Loading
- Run `collectstatic` again
- Check Nginx static file configuration
- Verify STATIC_ROOT path

### Database Connection Errors
- Verify database credentials
- Check PostgreSQL service status
- Ensure database exists

### Permission Denied
- Check file/directory permissions
- Verify user groups
- Check SELinux settings (if applicable)

---

For more help, see the [main README](README.md) or open an issue on GitHub.
