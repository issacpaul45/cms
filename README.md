# College Management System

## Introduction

The College Management System is a web-based application developed using the Python Django framework. It is designed to manage academic and administrative activities for a single batch in a department over three consecutive semesters. The system facilitates student and faculty management, academic progress tracking, and administrative automation.

## Features

### 1. Batch and Student Management

- Focuses on managing a single batch within a department.
- Students can be assigned to the batch at the beginning of each semester.
- Admin can add, update, or remove students from the batch.

### 2. Teacher and Subject Assignment

- Teachers are added and assigned to specific subjects each semester.
- Subjects can have one or more teachers based on department requirements.
- Teachers oversee academic activities related to their assigned subjects.

### 3. Assignment Creation and Submission

- Teachers can create and post assignments with descriptions, due dates, and guidelines.
- Students can view and submit assignments before deadlines.
- Teachers can review, provide feedback, and mark submissions.

### 4. Attendance and Marks Management

- Teachers can record student attendance for their respective subjects.
- Internal assessment marks (tests, assignments) are managed by teachers.
- The system calculates total internal marks based on assignments and tests.
- Students can log in to view their attendance and marks.

### 5. Top Scorer Tracking

- Displays the top scorer for each semester based on internal marks.
- Allows students to view highest scores for motivation and competition.

### 6. Fee Payment System

- Integrated module for online tuition fee payment.
- Students can check fee status (paid or pending) and make secure payments.

### 7. User Roles

- **Admin**: Manages users (teachers, students), subjects, and system configurations.
- **Teachers**: Manage assignments, attendance, and internal marks.
- **Students**: View assignments, submit work, track academic progress, and pay fees.

## Technologies Used

- **Frontend**: [![My Skills](https://skillicons.dev/icons?i=html,css,js,bootstrap)](https://skillicons.dev)
- **Backend**: [![My Skills](https://skillicons.dev/icons?i=python,django)](https://skillicons.dev)
- **Database**: [![My Skills](https://skillicons.dev/icons?i=sqlite)](https://skillicons.dev)
- **Payment Gateway Integration**: Third-party APIs for online fee payments

## Conclusion

The College Management System provides an efficient and user-friendly platform for managing academic progress and administrative activities for a specific batch. It automates assignment management, attendance tracking, and mark calculation while enabling students to stay updated on their academic standing and allowing seamless fee payments. This system enhances communication between students and teachers, improving the overall learning experience.

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd CMS
   ```
3. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```sh
   python manage.py migrate
   ```
6. Start the development server:
   ```sh
   python manage.py runserver
   ```
7. Open the application in a browser:
   ```
   http://127.0.0.1:8000/
   ```
