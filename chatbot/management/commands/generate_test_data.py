import random
from django.core.management.base import BaseCommand
from faker import Faker
import mysql.connector

class Command(BaseCommand):
    help = 'Generates 3000+ test records for the university database'

    def handle(self, *args, **options):
        fake = Faker()

        # Connect to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='univ_user',
            password='Univ@1234',
            database='university'
        )
        cursor = conn.cursor()

        # Clear existing test data (optional)
        cursor.execute("DELETE FROM enrollments")
        cursor.execute("DELETE FROM courses")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM professors")

        # 1. Insert Professors and collect IDs
        professor_ids = []
        for _ in range(500):
            name = fake.name()
            dept = random.choice(['CS', 'Math', 'Physics', 'Engineering', 'Biology'])
            title = random.choice(['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer'])
            cursor.execute(
                "INSERT INTO professors (professor_name, department, title) VALUES (%s, %s, %s)",
                (name, dept, title)
            )
            professor_ids.append(cursor.lastrowid)

        # 2. Insert Students and collect IDs
        student_ids = []
        for _ in range(3000):
            name = fake.name()
            major = random.choice(['CS', 'Math', 'Physics', 'Engineering', 'Biology'])
            dept = random.choice(['CS', 'Math', 'Physics', 'Engineering', 'Biology'])
            gpa = round(random.uniform(2.0, 4.0), 2)
            cursor.execute(
                "INSERT INTO students (student_name, major, department, gpa) VALUES (%s, %s, %s, %s)",
                (name, major, dept, gpa)
            )
            student_ids.append(cursor.lastrowid)

        # 3. Insert Courses and collect IDs
        course_ids = []
        course_names = [
            "Intro to Programming", "Databases", "Algorithms",
            "Calculus", "Linear Algebra", "Quantum Physics",
            "Genetics", "AI", "ML", "Operating Systems"
        ]
        for _ in range(100):
            name = f"{random.choice(course_names)} {random.randint(100, 499)}"
            credits = random.randint(3, 4)
            prof_id = random.choice(professor_ids)
            cursor.execute(
                "INSERT INTO courses (course_name, credits, professor_id) VALUES (%s, %s, %s)",
                (name, credits, prof_id)
            )
            course_ids.append(cursor.lastrowid)

        # 4. Insert Enrollments using real student/course IDs
        grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
        enrollments = []
        for student_id in student_ids:
            for _ in range(random.randint(3, 7)):
                course_id = random.choice(course_ids)
                grade = random.choice(grades)
                enrollments.append((student_id, course_id, grade))

        cursor.executemany(
            "INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)",
            enrollments
        )

        conn.commit()
        cursor.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('✔ Successfully generated 3000+ test records'))
