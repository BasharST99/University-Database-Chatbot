CREATE DATABASE IF NOT EXISTS university;
USE university;

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    major VARCHAR(100),
    department VARCHAR(100), 
    gpa DECIMAL(3,2)
);

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    professor_name VARCHAR(100),
    department VARCHAR(100),
    title VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT,
    professor_id INT,
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
