import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student

# Import your models

# Create and check models


def add_students():  # solution 1

    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com',
    )

    student2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com',
    )
    student2.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com',
    )

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com',
    )


# add_students()
# print(Student.objects.all())


def get_students_info():  # solution 2
    students_data = []
    for student in Student.objects.all():
        students_data.append(
            f"Student №{student.student_id}: "
            f"{student.first_name} "
            f"{student.last_name}; "
            f"Email: {student.email}"
        )
    return "\n".join(students_data)

# print(get_students_info())


def update_students_emails():  # solution 3
    for student in Student.objects.all():
        new_email = student.email.replace('university.com', 'uni-students.com')
        student.email = new_email
        student.save()
        print(student.email)


# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)


def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
