from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponse
from django.contrib import messages
from django.utils import timezone

from adminapp.models import Department,Teacher,Student,User,TeacherSubject,Subject
from Teacher.models import Add_assignment,Submission_assgn,Attendance,InternalAssessmentMarks
from Student.models import Submission
from datetime import date

# Create your views here.
def teacherhome(request):
    s =request.session.get('teach_id')
    user=User.objects.get(id=s)
    name=user.first_name +" "+ user.last_name 
    return render(request,'teacher/home.html',{'name':name})

def editteachprofile(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = Teacher.objects.get(teacher_id=user)
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        experience = request.POST['experience']
        username = request.POST['username']
        password = request.POST['password']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password:
            user.set_password(password)
        user.save()

        teacher.phone_number = phone_number
        teacher.address = address
        teacher.experience = experience
        teacher.save()

        messages.success(request, "Profile updated successfully...!!!")
        return redirect('teacherhome')

    context = {
        'user': user,
        'teacher': teacher,
        'dept': teacher.department_id,
    }
    return render(request, 'teacher/edit_profile.html', context)







# View assigned subjects
def view_subjects(request):
    # Get the teacher's ID from the session
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = Teacher.objects.get(teacher_id=user)

    # Fetch subjects assigned to the teacher
    assigned_subjects = TeacherSubject.objects.filter(teacher=teacher).select_related('subject')

    return render(request, 'teacher/viewteachersubject.html', {'assigned_subjects': assigned_subjects})


# Create an assignment
def create_assignment(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = Teacher.objects.get(teacher_id=user)

    if request.method == 'POST':
        subject_id = request.POST['subject_id']
        semester = request.POST['semester']
        description = request.POST['description']
        due_date = request.POST['due_date']

        subject = Subject.objects.get(id=subject_id)

        assignment = Add_assignment.objects.create(
            subject=subject,
            semester=semester,
            description=description,
            due_date=due_date
        )
        assignment.save()
        messages.success(request,'Asignment created Successfully...')
        return redirect('addassignment')
    assigned_subjects = TeacherSubject.objects.filter(teacher=teacher).select_related('subject')

    semesters = assigned_subjects.values_list('subject__semester', flat=True).distinct()

    return render(request, 'teacher/add_assignment.html', {
        'assigned_subjects': assigned_subjects,
        'semesters': semesters,
    })

#review the uploaded assignments

def view_submissions(request, assignment_id):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = Teacher.objects.get(teacher_id=user)

    assignment = get_object_or_404(Add_assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)

    return render(request, 'teacher/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
    })

def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        marks = request.POST.get('marks')
        
        submission.feedback = feedback
        submission.marks = marks
        submission.save()
        
        messages.success(request, "Feedback and marks added successfully.")
        return redirect('view_submissions', assignment_id=submission.assignment.id)

    return render(request, 'teacher/review_submission.html', {'submission': submission})


def teacher_assignments(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = Teacher.objects.get(teacher_id=user)

    # Get all subjects assigned to the teacher
    assigned_subjects = TeacherSubject.objects.filter(teacher=teacher).values_list('subject', flat=True)

    # Get all assignments created for the subjects the teacher teaches
    assignments = Add_assignment.objects.filter(subject__in=assigned_subjects)

    return render(request, 'teacher/view_all_assignments.html', {'assignments': assignments})



def view_attendance(request):
    # Get the teacher's ID from the session
    teacher_id = request.session.get('teach_id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)

    # Fetch subjects assigned to the teacher
    assigned_subjects = TeacherSubject.objects.filter(teacher=teacher).select_related('subject')

    # List to store students for each subject
    students_data = []

    # Fetch the selected date or use today as default
    selected_date = request.POST.get('attendance_date', str(date.today()))
    today = date.fromisoformat(selected_date)

    # For each subject assigned to the teacher, get students and attendance data
    for assigned_subject in assigned_subjects:
        students_in_subject = Student.objects.filter(department_id=teacher.department_id, semester=assigned_subject.subject.semester)
        
        # Check if attendance has already been marked for each student on the selected date
        attendance_data = {}
        for student in students_in_subject:
            # Retrieve attendance for the specific date
            attendance = Attendance.objects.filter(
                teacher=teacher, student=student, subject=assigned_subject.subject, date=today
            ).first()
            # Store attendance data (True if marked, False otherwise)
            attendance_data[student.id] = attendance  # We store the actual attendance object, or None if not found
        
        students_data.append({
            'subject': assigned_subject.subject,
            'students': students_in_subject,
            'attendance_data': attendance_data
        })

    # If form is submitted, mark attendance
    if request.method == 'POST':
        for student in students_data:
            subject = student['subject']
            for stud in student['students']:
                # Capture the attendance status from POST data
                attendance_status = request.POST.get(f'attendance_{stud.id}_{subject.id}')
                if attendance_status is not None:
                    status = 'Present' if attendance_status == 'present' else 'Absent'
                    # Check if the attendance is already marked for today; if so, update, otherwise create
                    attendance, created = Attendance.objects.get_or_create(
                        teacher=teacher, student=stud, subject=subject, date=today
                    )
                    attendance.status = status
                    attendance.save()

        messages.success(request, "Attendance marked successfully.")
        return redirect('view_attnd')

    return render(request, 'teacher/mark_attendance.html', {'students_data': students_data, 'today': today})



def record_marks(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = get_object_or_404(Teacher, teacher_id=user)

    teacher_subjects = TeacherSubject.objects.filter(teacher=teacher).select_related('subject')
    semesters = teacher_subjects.values_list('subject__semester', flat=True).distinct()

    selected_semester = request.GET.get('semester')
    students = []
    filtered_subjects = []

    if selected_semester:
        filtered_subjects = teacher_subjects.filter(subject__semester=selected_semester)
        students = Student.objects.filter(department_id=teacher.department_id, semester=selected_semester)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        assessment_type = request.POST.get('assessment_type')
        marks_obtained = request.POST.get('marks_obtained')
        max_marks = request.POST.get('max_marks')

        if not (student_id and subject_id and assessment_type and marks_obtained and max_marks):
            messages.error(request, "All fields are required.")
            return redirect('record_marks')

        try:
            marks_obtained = int(marks_obtained)
            max_marks = int(max_marks)

            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)

            marks, created = InternalAssessmentMarks.objects.get_or_create(
                student=student,
                subject=subject,
                teacher=teacher,
                assessment_type=assessment_type,
                defaults={'marks_obtained': marks_obtained, 'max_marks': max_marks}
            )
            if not created:
                marks.marks_obtained = marks_obtained
                marks.max_marks = max_marks
                marks.save()

            messages.success(request, "Marks recorded successfully!")
            return redirect('record_marks')
        except ValueError:
            messages.error(request, "Invalid marks entered. Please enter valid integers.")
            return redirect('record_marks')

    return render(request, 'teacher/record_marks.html', {
        'students': students,
        'semesters': semesters,
        'selected_semester': selected_semester,
        'subjects': [ts.subject for ts in filtered_subjects],
        'assessment_choices': InternalAssessmentMarks.ASSESSMENT_CHOICES,  # Now passing assessment type choices
    })


def view_student_marks(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = get_object_or_404(Teacher, teacher_id=user)

    students = Student.objects.filter(department_id=teacher.department_id)

    student_marks = {}

    for student in students:
        marks = InternalAssessmentMarks.objects.filter(student=student)
        total_marks_obtained = sum(mark.marks_obtained for mark in marks)
        total_max_marks = sum(mark.max_marks for mark in marks)

        student_marks[student] = {
            'marks': marks,
            'total_marks_obtained': total_marks_obtained,
            'total_max_marks': total_max_marks,
        }

    return render(request, 'teacher/view_student_marks.html', {
        'student_marks': student_marks,
    })

def generate_student_record(request):
    s = request.session.get('teach_id')
    user = User.objects.get(id=s)
    teacher = get_object_or_404(Teacher, teacher_id=user)

    # Get subjects assigned to the teacher
    teacher_subjects = TeacherSubject.objects.filter(teacher=teacher).select_related('subject')
    semesters = teacher_subjects.values_list('subject__semester', flat=True).distinct()

    selected_semester = None
    student_marks = []

    if request.method == 'POST':
        selected_semester = request.POST.get('semester')

        if selected_semester:
            # Get students in the selected semester
            students = Student.objects.filter(department_id=teacher.department_id, semester=selected_semester)

            for student in students:
                marks = InternalAssessmentMarks.objects.filter(student=student, subject__in=teacher_subjects.filter(subject__semester=selected_semester).values_list('subject', flat=True))
                total_marks_obtained = sum(mark.marks_obtained for mark in marks)
                total_max_marks = sum(mark.max_marks for mark in marks)

                student_marks.append({
                    'student': student,
                    'marks': marks,
                    'total_marks_obtained': total_marks_obtained,
                    'total_max_marks': total_max_marks,
                })

    return render(request, 'teacher/generate_student_record.html', {
        'semesters': semesters,
        'student_marks': student_marks,
        'selected_semester': selected_semester,
    })