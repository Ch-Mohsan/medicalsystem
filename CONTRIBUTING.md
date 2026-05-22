# Contributing to MediConnect

First off, thank you for considering contributing to MediConnect! It's people like you that make MediConnect such a great tool.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Your environment** (OS, Python version, Django version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List examples** of how it would be used

### Your First Code Contribution

Unsure where to begin? You can start by looking through:
- `beginner` labeled issues
- `good-first-issue` labeled issues
- `help-wanted` labeled issues

### Pull Requests

- Fill in the required template
- Follow the coding standards
- Include appropriate test cases
- Update documentation as needed
- Ensure all tests pass

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/mediconnect.git
cd mediconnect

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/mediconnect.git
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to project directory
cd myproject

# Setup database
python manage.py migrate

# Load sample data
python manage.py populate_data
```

### 3. Create a Branch

```bash
# Create a branch for your feature
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

## 📝 Coding Standards

### Python/Django Style

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **119 characters**
- Use **snake_case** for function and variable names
- Use **PascalCase** for class names

### Code Structure

```python
# Good
def get_doctor_appointments(doctor_id, status=None):
    """
    Retrieve appointments for a specific doctor.
    
    Args:
        doctor_id (int): The ID of the doctor
        status (str, optional): Filter by appointment status
        
    Returns:
        QuerySet: Filtered appointments
    """
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    if status:
        appointments = appointments.filter(status=status)
    return appointments
```

### Naming Conventions

- **Models**: Singular noun (e.g., `Doctor`, `Appointment`)
- **Views**: Descriptive verb/noun (e.g., `book_appointment`, `doctor_dashboard`)
- **URLs**: Lowercase with hyphens (e.g., `book-appointment`)
- **Templates**: Lowercase with underscores (e.g., `doctor_detail.html`)

### Documentation

- Add docstrings to all functions and classes
- Comment complex logic
- Update README.md if adding new features
- Create/update API documentation if applicable

### Django Best Practices

- Use Django ORM (avoid raw SQL)
- Use `get_object_or_404` for object retrieval
- Use Django forms for validation
- Implement proper error handling
- Use Django's built-in authentication
- Follow Django's file structure conventions

## 🏷️ Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no code change)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples

```
feat(appointments): Add appointment cancellation feature

- Added cancel button in patient appointments
- Implemented api_cancel_appointment endpoint
- Updated appointment model with cancellation timestamp

Closes #123
```

```
fix(doctor-profile): Fix profile image upload issue

Fixed issue where profile images weren't saving correctly
due to incorrect MEDIA_ROOT configuration.

Fixes #456
```

```
docs(readme): Update installation instructions

Added more detailed steps for Windows users and
troubleshooting section for common setup issues.
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Run tests**
   ```bash
   python manage.py test
   ```

3. **Check code style**
   ```bash
   flake8 Mediconnect/
   ```

4. **Update documentation** if needed

### Submit Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Use a clear title
   - Reference related issues
   - Describe changes in detail
   - Add screenshots if UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   
   ## Related Issues
   Fixes #123
   
   ## Testing
   Describe how you tested the changes
   
   ## Screenshots (if applicable)
   Add screenshots here
   
   ## Checklist
   - [ ] My code follows the project's style guidelines
   - [ ] I have commented my code where necessary
   - [ ] I have updated the documentation
   - [ ] My changes generate no new warnings
   - [ ] I have added tests that prove my fix/feature works
   - [ ] New and existing tests pass locally
   ```

### Review Process

- At least one maintainer will review your PR
- Address any requested changes
- Once approved, a maintainer will merge your PR

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test Mediconnect

# Run specific test case
python manage.py test Mediconnect.tests.TestAppointment

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

```python
from django.test import TestCase
from .models import Doctor, Patient

class AppointmentTestCase(TestCase):
    def setUp(self):
        # Setup test data
        self.doctor = Doctor.objects.create(...)
        self.patient = Patient.objects.create(...)
    
    def test_appointment_creation(self):
        """Test that appointments can be created successfully"""
        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            # ... other fields
        )
        self.assertIsNotNone(appointment.id)
        self.assertEqual(appointment.status, 'pending')
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Commit Message Guidelines](https://chris.beams.io/posts/git-commit/)

## 🐛 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good-first-issue`: Good for newcomers
- `help-wanted`: Extra attention is needed
- `question`: Further information is requested

## 💡 Feature Requests

We track feature requests as GitHub issues. Create an issue with:

- Clear title describing the feature
- Detailed description of the feature
- Use cases and benefits
- Any implementation ideas

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Special mentions for significant contributions

## 📧 Questions?

Feel free to:
- Open a GitHub issue with the `question` label
- Reach out to maintainers
- Check existing documentation

---

Thank you for contributing to MediConnect! 🏥💙
