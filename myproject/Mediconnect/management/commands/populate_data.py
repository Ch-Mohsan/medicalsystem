from django.core.management.base import BaseCommand
from datetime import date, time, timedelta
from ...models import User, Patient, Doctor, Specialization, TimeSlot, Appointment, Review, Contact


class Command(BaseCommand):
    help = 'Populate database with Pakistani sample data'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(" MEDICONNECT - COMPLETE DATA POPULATION "))
        self.stdout.write("=" * 60 + "\n")

        # Clear all data
        self.stdout.write("Clearing all existing data...")
        Review.objects.all().delete()
        Appointment.objects.all().delete()
        TimeSlot.objects.all().delete()
        Doctor.objects.all().delete()
        Specialization.objects.all().delete()
        Patient.objects.all().delete()
        Contact.objects.all().delete()
        User.objects.filter(user_type__in=['patient', 'doctor']).delete()
        self.stdout.write(self.style.SUCCESS("✓ All data cleared\n"))

        # Create data
        users = self.create_users()
        patients = self.create_patients(users)
        specializations = self.create_specializations()
        doctors = self.create_doctors(users, specializations)
        self.create_time_slots(doctors)
        self.create_appointments(patients, doctors)
        self.create_reviews(patients, doctors)
        self.create_contacts()

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(" DATA POPULATION COMPLETED SUCCESSFULLY! "))
        self.stdout.write("=" * 60)
        self.stdout.write("\nSummary:")
        self.stdout.write("  • Users: 20 (10 patients + 10 doctors)")
        self.stdout.write("  • Patient Profiles: 10")
        self.stdout.write("  • Specializations: 10")
        self.stdout.write("  • Doctor Profiles: 10")
        self.stdout.write("  • Time Slots: 80 (8 per doctor)")
        self.stdout.write("  • Appointments: 12")
        self.stdout.write("  • Reviews: 10")
        self.stdout.write("  • Contact Messages: 5")
        self.stdout.write("\nLogin Credentials:")
        self.stdout.write(self.style.WARNING("  Patient: ahmed.khan@gmail.com / patient123"))
        self.stdout.write(self.style.WARNING("  Doctor: dr.asim.malik@gmail.com / doctor123"))
        self.stdout.write("=" * 60 + "\n")

    def create_users(self):
        self.stdout.write("\nSTEP 1: Creating Users")
        self.stdout.write("-" * 60)

        patient_data = [
            {'email': 'ahmed.khan@gmail.com', 'first_name': 'Ahmed', 'last_name': 'Khan', 'phone': '0300-1234567'},
            {'email': 'fatima.ali@gmail.com', 'first_name': 'Fatima', 'last_name': 'Ali', 'phone': '0321-2345678'},
            {'email': 'usman.malik@gmail.com', 'first_name': 'Usman', 'last_name': 'Malik', 'phone': '0333-3456789'},
            {'email': 'ayesha.ahmad@gmail.com', 'first_name': 'Ayesha', 'last_name': 'Ahmad', 'phone': '0300-4567890'},
            {'email': 'bilal.hussain@gmail.com', 'first_name': 'Bilal', 'last_name': 'Hussain', 'phone': '0345-5678901'},
            {'email': 'zainab.sheikh@gmail.com', 'first_name': 'Zainab', 'last_name': 'Sheikh', 'phone': '0312-6789012'},
            {'email': 'hassan.raza@gmail.com', 'first_name': 'Hassan', 'last_name': 'Raza', 'phone': '0301-7890123'},
            {'email': 'maryam.hassan@gmail.com', 'first_name': 'Maryam', 'last_name': 'Hassan', 'phone': '0333-8901234'},
            {'email': 'ali.aslam@gmail.com', 'first_name': 'Ali', 'last_name': 'Aslam', 'phone': '0320-9012345'},
            {'email': 'sana.farooq@gmail.com', 'first_name': 'Sana', 'last_name': 'Farooq', 'phone': '0300-0123456'},
        ]

        users = {}
        for data in patient_data:
            user = User.objects.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password='patient123',
                user_type='patient',
                phone=data['phone']
            )
            users[data['email']] = user

        doctor_data = [
            {'email': 'dr.asim.malik@gmail.com', 'first_name': 'Dr. Asim', 'last_name': 'Malik', 'phone': '0300-1111111'},
            {'email': 'dr.sarah.ahmed@gmail.com', 'first_name': 'Dr. Sarah', 'last_name': 'Ahmed', 'phone': '0321-2222222'},
            {'email': 'dr.kamran.shah@gmail.com', 'first_name': 'Dr. Kamran', 'last_name': 'Shah', 'phone': '0333-3333333'},
            {'email': 'dr.nadia.khan@gmail.com', 'first_name': 'Dr. Nadia', 'last_name': 'Khan', 'phone': '0300-4444444'},
            {'email': 'dr.tariq.mehmood@gmail.com', 'first_name': 'Dr. Tariq', 'last_name': 'Mehmood', 'phone': '0345-5555555'},
            {'email': 'dr.hina.abbasi@gmail.com', 'first_name': 'Dr. Hina', 'last_name': 'Abbasi', 'phone': '0312-6666666'},
            {'email': 'dr.imran.siddiqui@gmail.com', 'first_name': 'Dr. Imran', 'last_name': 'Siddiqui', 'phone': '0301-7777777'},
            {'email': 'dr.amna.yousaf@gmail.com', 'first_name': 'Dr. Amna', 'last_name': 'Yousaf', 'phone': '0333-8888888'},
            {'email': 'dr.faisal.iqbal@gmail.com', 'first_name': 'Dr. Faisal', 'last_name': 'Iqbal', 'phone': '0320-9999999'},
            {'email': 'dr.rabia.saleem@gmail.com', 'first_name': 'Dr. Rabia', 'last_name': 'Saleem', 'phone': '0300-0000000'},
        ]

        for data in doctor_data:
            user = User.objects.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password='doctor123',
                user_type='doctor',
                phone=data['phone']
            )
            users[data['email']] = user

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(users)} users (10 patients + 10 doctors)"))
        return users

    def create_patients(self, users):
        self.stdout.write("\nSTEP 2: Creating Patient Profiles")
        self.stdout.write("-" * 60)

        patient_details = [
            {'email': 'ahmed.khan@gmail.com', 'date_of_birth': date(1990, 5, 15), 'gender': 'Male', 'blood_group': 'B+', 'height': '5.8', 'weight': '70', 'address': 'House 123, Street 10, F-7/2, Islamabad', 'allergies': 'Penicillin', 'current_medication': 'None', 'emergency_contact': '0333-9876543'},
            {'email': 'fatima.ali@gmail.com', 'date_of_birth': date(1995, 8, 22), 'gender': 'Female', 'blood_group': 'A+', 'height': '5.4', 'weight': '55', 'address': 'Flat 45, Block B, Gulshan-e-Iqbal, Karachi', 'allergies': 'None', 'current_medication': 'Multivitamins', 'emergency_contact': '0321-8765432'},
            {'email': 'usman.malik@gmail.com', 'date_of_birth': date(1988, 3, 10), 'gender': 'Male', 'blood_group': 'O+', 'height': '6.0', 'weight': '80', 'address': 'House 456, Model Town, Lahore', 'allergies': 'Dust', 'current_medication': 'Blood pressure medication', 'emergency_contact': '0300-7654321'},
            {'email': 'ayesha.ahmad@gmail.com', 'date_of_birth': date(1992, 11, 5), 'gender': 'Female', 'blood_group': 'AB+', 'height': '5.5', 'weight': '58', 'address': 'Apartment 12, DHA Phase 5, Karachi', 'allergies': 'Pollen', 'current_medication': 'None', 'emergency_contact': '0345-6543210'},
            {'email': 'bilal.hussain@gmail.com', 'date_of_birth': date(1985, 7, 18), 'gender': 'Male', 'blood_group': 'B-', 'height': '5.9', 'weight': '75', 'address': 'House 789, Satellite Town, Rawalpindi', 'allergies': 'Shellfish', 'current_medication': 'Diabetes medication', 'emergency_contact': '0312-5432109'},
            {'email': 'zainab.sheikh@gmail.com', 'date_of_birth': date(1998, 2, 28), 'gender': 'Female', 'blood_group': 'O-', 'height': '5.3', 'weight': '52', 'address': 'House 321, Johar Town, Lahore', 'allergies': 'None', 'current_medication': 'Iron supplements', 'emergency_contact': '0301-4321098'},
            {'email': 'hassan.raza@gmail.com', 'date_of_birth': date(1991, 9, 12), 'gender': 'Male', 'blood_group': 'A-', 'height': '5.10', 'weight': '78', 'address': 'Flat 67, Nazimabad, Karachi', 'allergies': 'Latex', 'current_medication': 'None', 'emergency_contact': '0333-3210987'},
            {'email': 'maryam.hassan@gmail.com', 'date_of_birth': date(1994, 6, 25), 'gender': 'Female', 'blood_group': 'B+', 'height': '5.6', 'weight': '60', 'address': 'House 555, Bahria Town, Islamabad', 'allergies': 'Aspirin', 'current_medication': 'Thyroid medication', 'emergency_contact': '0320-2109876'},
            {'email': 'ali.aslam@gmail.com', 'date_of_birth': date(1987, 4, 8), 'gender': 'Male', 'blood_group': 'AB-', 'height': '5.11', 'weight': '82', 'address': 'House 888, Cavalry Ground, Lahore', 'allergies': 'None', 'current_medication': 'None', 'emergency_contact': '0300-1098765'},
            {'email': 'sana.farooq@gmail.com', 'date_of_birth': date(1996, 12, 3), 'gender': 'Female', 'blood_group': 'A+', 'height': '5.4', 'weight': '54', 'address': 'Apartment 23, Clifton, Karachi', 'allergies': 'Sulfa drugs', 'current_medication': 'Contraceptives', 'emergency_contact': '0321-0987654'},
        ]

        patients = {}
        for detail in patient_details:
            user = users[detail['email']]
            patient = Patient.objects.create(
                user=user,
                date_of_birth=detail['date_of_birth'],
                gender=detail['gender'],
                blood_group=detail['blood_group'],
                height=detail['height'],
                weight=detail['weight'],
                address=detail['address'],
                allergies=detail['allergies'],
                current_medication=detail['current_medication'],
                emergency_contact=detail['emergency_contact']
            )
            patients[detail['email']] = patient

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(patients)} patient profiles"))
        return patients

    def create_specializations(self):
        self.stdout.write("\nSTEP 3: Creating Specializations")
        self.stdout.write("-" * 60)

        specializations_data = [
            {'name': 'Cardiology', 'description': 'Diagnosis and treatment of heart conditions'},
            {'name': 'Dermatology', 'description': 'Treatment of skin, hair, and nail disorders'},
            {'name': 'Orthopedics', 'description': 'Treatment of musculoskeletal system'},
            {'name': 'Pediatrics', 'description': 'Medical care for infants, children, and adolescents'},
            {'name': 'Gynecology', 'description': 'Women\'s reproductive health'},
            {'name': 'Neurology', 'description': 'Treatment of nervous system disorders'},
            {'name': 'ENT', 'description': 'Ear, Nose, and Throat specialist'},
            {'name': 'Dentistry', 'description': 'Oral health and dental care'},
            {'name': 'General Medicine', 'description': 'Primary healthcare and general medical conditions'},
            {'name': 'Psychiatry', 'description': 'Mental health and behavioral disorders'},
        ]

        specializations = {}
        for spec_data in specializations_data:
            spec = Specialization.objects.create(**spec_data)
            specializations[spec_data['name']] = spec

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(specializations)} specializations"))
        return specializations

    def create_doctors(self, users, specializations):
        self.stdout.write("\nSTEP 4: Creating Doctor Profiles")
        self.stdout.write("-" * 60)

        doctor_details = [
            {'email': 'dr.asim.malik@gmail.com', 'license_number': 'PMC-12345', 'qualification': 'MBBS, FCPS (Cardiology)', 'experience_years': 15, 'consultation_fee': 3000, 'rating': 4.8, 'clinic_name': 'Malik Heart Center', 'clinic_address': 'Plot 123, F-6/2, Islamabad', 'specialization': 'Cardiology', 'bio': 'Experienced cardiologist with expertise in cardiac interventions and heart disease management.'},
            {'email': 'dr.sarah.ahmed@gmail.com', 'license_number': 'PMC-23456', 'qualification': 'MBBS, FCPS (Dermatology)', 'experience_years': 10, 'consultation_fee': 2500, 'rating': 4.7, 'clinic_name': 'Skin Care Clinic', 'clinic_address': 'Shop 45, Tariq Road, Karachi', 'specialization': 'Dermatology', 'bio': 'Specialist in cosmetic dermatology and treatment of chronic skin conditions.'},
            {'email': 'dr.kamran.shah@gmail.com', 'license_number': 'PMC-34567', 'qualification': 'MBBS, MS (Orthopedics)', 'experience_years': 12, 'consultation_fee': 2800, 'rating': 4.6, 'clinic_name': 'Bone & Joint Center', 'clinic_address': 'Block E, Model Town, Lahore', 'specialization': 'Orthopedics', 'bio': 'Expert in joint replacement surgery and sports injuries.'},
            {'email': 'dr.nadia.khan@gmail.com', 'license_number': 'PMC-45678', 'qualification': 'MBBS, DCH, FCPS (Pediatrics)', 'experience_years': 8, 'consultation_fee': 2000, 'rating': 4.9, 'clinic_name': 'Little Angels Pediatric Clinic', 'clinic_address': 'House 567, G-10/4, Islamabad', 'specialization': 'Pediatrics', 'bio': 'Dedicated pediatrician with special interest in child nutrition and development.'},
            {'email': 'dr.tariq.mehmood@gmail.com', 'license_number': 'PMC-56789', 'qualification': 'MBBS, FCPS (Gynecology)', 'experience_years': 18, 'consultation_fee': 3500, 'rating': 4.8, 'clinic_name': 'Women\'s Health Center', 'clinic_address': 'Plot 234, DHA Phase 6, Karachi', 'specialization': 'Gynecology', 'bio': 'Senior gynecologist specializing in high-risk pregnancies and women\'s health.'},
            {'email': 'dr.hina.abbasi@gmail.com', 'license_number': 'PMC-67890', 'qualification': 'MBBS, FCPS (Neurology)', 'experience_years': 11, 'consultation_fee': 3200, 'rating': 4.7, 'clinic_name': 'Neuro Care Center', 'clinic_address': 'Canal Road, Lahore', 'specialization': 'Neurology', 'bio': 'Neurologist with expertise in stroke management and epilepsy treatment.'},
            {'email': 'dr.imran.siddiqui@gmail.com', 'license_number': 'PMC-78901', 'qualification': 'MBBS, FCPS (ENT)', 'experience_years': 9, 'consultation_fee': 2200, 'rating': 4.5, 'clinic_name': 'ENT Specialists', 'clinic_address': 'Street 15, F-8 Markaz, Islamabad', 'specialization': 'ENT', 'bio': 'ENT surgeon specializing in endoscopic sinus surgery and hearing disorders.'},
            {'email': 'dr.amna.yousaf@gmail.com', 'license_number': 'PMC-89012', 'qualification': 'BDS, FCPS (Dentistry)', 'experience_years': 7, 'consultation_fee': 1800, 'rating': 4.8, 'clinic_name': 'Smile Dental Clinic', 'clinic_address': 'MM Alam Road, Lahore', 'specialization': 'Dentistry', 'bio': 'Dental surgeon with expertise in cosmetic dentistry and implants.'},
            {'email': 'dr.faisal.iqbal@gmail.com', 'license_number': 'PMC-90123', 'qualification': 'MBBS, MCPS', 'experience_years': 14, 'consultation_fee': 1500, 'rating': 4.6, 'clinic_name': 'Family Health Clinic', 'clinic_address': 'Sector 11, North Karachi, Karachi', 'specialization': 'General Medicine', 'bio': 'General practitioner providing comprehensive primary healthcare services.'},
            {'email': 'dr.rabia.saleem@gmail.com', 'license_number': 'PMC-01234', 'qualification': 'MBBS, FCPS (Psychiatry)', 'experience_years': 6, 'consultation_fee': 2500, 'rating': 4.9, 'clinic_name': 'Mind Wellness Center', 'clinic_address': 'Blue Area, Islamabad', 'specialization': 'Psychiatry', 'bio': 'Psychiatrist specializing in anxiety, depression, and behavioral disorders.'},
        ]

        doctors = {}
        for detail in doctor_details:
            user = users[detail['email']]
            doctor = Doctor.objects.create(
                user=user,
                license_number=detail['license_number'],
                qualification=detail['qualification'],
                experience_years=detail['experience_years'],
                consultation_fee=detail['consultation_fee'],
                rating=detail['rating'],
                clinic_name=detail['clinic_name'],
                clinic_address=detail['clinic_address'],
                specialization=specializations[detail['specialization']],
                bio=detail['bio']
            )
            doctors[detail['email']] = doctor

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(doctors)} doctor profiles"))
        return doctors

    def create_time_slots(self, doctors):
        self.stdout.write("\nSTEP 5: Creating Time Slots")
        self.stdout.write("-" * 60)

        time_slots_data = [
            {'start': time(9, 0), 'end': time(10, 0)},
            {'start': time(10, 0), 'end': time(11, 0)},
            {'start': time(11, 0), 'end': time(12, 0)},
            {'start': time(14, 0), 'end': time(15, 0)},
            {'start': time(15, 0), 'end': time(16, 0)},
            {'start': time(16, 0), 'end': time(17, 0)},
            {'start': time(17, 0), 'end': time(18, 0)},
            {'start': time(18, 0), 'end': time(19, 0)},
        ]

        count = 0
        for doctor in doctors.values():
            for slot in time_slots_data:
                TimeSlot.objects.create(
                    doctor=doctor,
                    start_time=slot['start'],
                    end_time=slot['end']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {count} time slots (8 per doctor)"))

    def create_appointments(self, patients, doctors):
        self.stdout.write("\nSTEP 6: Creating Appointments")
        self.stdout.write("-" * 60)

        today = date.today()
        appointments_data = [
            {'patient_email': 'ahmed.khan@gmail.com', 'doctor_email': 'dr.asim.malik@gmail.com', 'appointment_date': today + timedelta(days=2), 'time_slot': '09:00 - 10:00', 'status': 'confirmed', 'reason': 'Chest pain and irregular heartbeat'},
            {'patient_email': 'fatima.ali@gmail.com', 'doctor_email': 'dr.sarah.ahmed@gmail.com', 'appointment_date': today + timedelta(days=1), 'time_slot': '10:00 - 11:00', 'status': 'confirmed', 'reason': 'Acne treatment and skin consultation'},
            {'patient_email': 'usman.malik@gmail.com', 'doctor_email': 'dr.kamran.shah@gmail.com', 'appointment_date': today + timedelta(days=3), 'time_slot': '11:00 - 12:00', 'status': 'pending', 'reason': 'Knee pain after sports injury'},
            {'patient_email': 'ayesha.ahmad@gmail.com', 'doctor_email': 'dr.nadia.khan@gmail.com', 'appointment_date': today + timedelta(days=5), 'time_slot': '14:00 - 15:00', 'status': 'confirmed', 'reason': 'Child vaccination and checkup'},
            {'patient_email': 'bilal.hussain@gmail.com', 'doctor_email': 'dr.faisal.iqbal@gmail.com', 'appointment_date': today + timedelta(days=1), 'time_slot': '15:00 - 16:00', 'status': 'confirmed', 'reason': 'Diabetes follow-up and blood pressure check'},
            {'patient_email': 'zainab.sheikh@gmail.com', 'doctor_email': 'dr.tariq.mehmood@gmail.com', 'appointment_date': today + timedelta(days=7), 'time_slot': '10:00 - 11:00', 'status': 'pending', 'reason': 'Gynecological consultation'},
            {'patient_email': 'hassan.raza@gmail.com', 'doctor_email': 'dr.imran.siddiqui@gmail.com', 'appointment_date': today + timedelta(days=4), 'time_slot': '16:00 - 17:00', 'status': 'confirmed', 'reason': 'Sinus infection and hearing problem'},
            {'patient_email': 'maryam.hassan@gmail.com', 'doctor_email': 'dr.hina.abbasi@gmail.com', 'appointment_date': today + timedelta(days=6), 'time_slot': '09:00 - 10:00', 'status': 'pending', 'reason': 'Frequent headaches and migraines'},
            {'patient_email': 'ali.aslam@gmail.com', 'doctor_email': 'dr.amna.yousaf@gmail.com', 'appointment_date': today + timedelta(days=2), 'time_slot': '17:00 - 18:00', 'status': 'confirmed', 'reason': 'Teeth cleaning and dental checkup'},
            {'patient_email': 'sana.farooq@gmail.com', 'doctor_email': 'dr.rabia.saleem@gmail.com', 'appointment_date': today + timedelta(days=3), 'time_slot': '11:00 - 12:00', 'status': 'pending', 'reason': 'Anxiety and stress management'},
            {'patient_email': 'ahmed.khan@gmail.com', 'doctor_email': 'dr.faisal.iqbal@gmail.com', 'appointment_date': today - timedelta(days=10), 'time_slot': '14:00 - 15:00', 'status': 'confirmed', 'reason': 'General checkup'},
            {'patient_email': 'fatima.ali@gmail.com', 'doctor_email': 'dr.nadia.khan@gmail.com', 'appointment_date': today - timedelta(days=5), 'time_slot': '15:00 - 16:00', 'status': 'confirmed', 'reason': 'Pediatric consultation'},
        ]

        for appt_data in appointments_data:
            doctor = doctors[appt_data['doctor_email']]
            Appointment.objects.create(
                patient=patients[appt_data['patient_email']],
                doctor=doctor,
                appointment_date=appt_data['appointment_date'],
                time_slot=appt_data['time_slot'],
                status=appt_data['status'],
                consultation_fee=str(doctor.consultation_fee),
                reason=appt_data['reason']
            )

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(appointments_data)} appointments"))

    def create_reviews(self, patients, doctors):
        self.stdout.write("\nSTEP 7: Creating Reviews")
        self.stdout.write("-" * 60)

        reviews_data = [
            {'patient_email': 'ahmed.khan@gmail.com', 'doctor_email': 'dr.asim.malik@gmail.com', 'rating': 5, 'comment': 'Excellent doctor! Very professional and caring. Explained everything clearly.'},
            {'patient_email': 'fatima.ali@gmail.com', 'doctor_email': 'dr.sarah.ahmed@gmail.com', 'rating': 5, 'comment': 'Dr. Sarah is amazing! My skin condition improved significantly after her treatment.'},
            {'patient_email': 'usman.malik@gmail.com', 'doctor_email': 'dr.kamran.shah@gmail.com', 'rating': 4, 'comment': 'Good experience. Wait time was a bit long but the consultation was thorough.'},
            {'patient_email': 'ayesha.ahmad@gmail.com', 'doctor_email': 'dr.nadia.khan@gmail.com', 'rating': 5, 'comment': 'Very kind and patient with children. Highly recommend for pediatric care.'},
            {'patient_email': 'bilal.hussain@gmail.com', 'doctor_email': 'dr.faisal.iqbal@gmail.com', 'rating': 4, 'comment': 'Knowledgeable doctor. Provides good advice for chronic conditions.'},
            {'patient_email': 'hassan.raza@gmail.com', 'doctor_email': 'dr.imran.siddiqui@gmail.com', 'rating': 4, 'comment': 'Helped me with my sinus problem. Treatment was effective.'},
            {'patient_email': 'ali.aslam@gmail.com', 'doctor_email': 'dr.amna.yousaf@gmail.com', 'rating': 5, 'comment': 'Best dentist in town! Painless treatment and great results.'},
            {'patient_email': 'sana.farooq@gmail.com', 'doctor_email': 'dr.rabia.saleem@gmail.com', 'rating': 5, 'comment': 'Dr. Rabia is very understanding and helpful. My anxiety has improved a lot.'},
            {'patient_email': 'fatima.ali@gmail.com', 'doctor_email': 'dr.asim.malik@gmail.com', 'rating': 4, 'comment': 'Professional service. Clinic is well-maintained and staff is courteous.'},
            {'patient_email': 'ahmed.khan@gmail.com', 'doctor_email': 'dr.faisal.iqbal@gmail.com', 'rating': 4, 'comment': 'Good general practitioner. Affordable and accessible.'},
        ]

        for review_data in reviews_data:
            Review.objects.create(
                patient=patients[review_data['patient_email']],
                doctor=doctors[review_data['doctor_email']],
                rating=review_data['rating'],
                comment=review_data['comment']
            )

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(reviews_data)} reviews"))

    def create_contacts(self):
        self.stdout.write("\nSTEP 8: Creating Contact Messages")
        self.stdout.write("-" * 60)

        contacts_data = [
            {'first_name': 'Kashif', 'last_name': 'Mahmood', 'email': 'kashif.mahmood@gmail.com', 'phone': '0300-1122334', 'subject': 'General Inquiry', 'message': 'I want to know about the specializations available on your platform.'},
            {'first_name': 'Nimra', 'last_name': 'Tariq', 'email': 'nimra.tariq@gmail.com', 'phone': '0321-2233445', 'subject': 'Technical Support', 'message': 'I am having trouble logging into my account. Please help.'},
            {'first_name': 'Adnan', 'last_name': 'Qureshi', 'email': 'adnan.qureshi@gmail.com', 'phone': '0333-3344556', 'subject': 'Appointment Help', 'message': 'How can I reschedule my appointment?'},
            {'first_name': 'Sidra', 'last_name': 'Naseem', 'email': 'sidra.naseem@gmail.com', 'phone': '0345-4455667', 'subject': 'Partnership Opportunity', 'message': 'I am a doctor and would like to join your platform. What is the process?'},
            {'first_name': 'Hamza', 'last_name': 'Aziz', 'email': 'hamza.aziz@gmail.com', 'phone': '0312-5566778', 'subject': 'Billing Question', 'message': 'I was charged twice for my last appointment. Please check.'},
        ]

        for contact_data in contacts_data:
            Contact.objects.create(**contact_data)

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(contacts_data)} contact messages"))
