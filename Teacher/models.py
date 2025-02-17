from django.db import models
from adminapp.models import User,TeacherSubject,Teacher,Student,Department,Subject
# Create your models here.

class Add_assignment(models.Model):
    subject  = models.ForeignKey(Subject,on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    description =models.TextField()
    doc = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()


class Submission_assgn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Add_assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    feedback = models.TextField(null=True, blank=True)  # New field for feedback
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # New field for marks
    
    class Meta:
        unique_together = ('student', 'assignment')



class Attendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)  # True for present, False for absent

    class Meta:
        unique_together = ('teacher', 'student', 'subject', 'date')


class InternalAssessmentMarks(models.Model):
    ASSESSMENT_CHOICES = [
        ('Internal Exam 1', 'Internal Exam 1'),
        ('Internal Exam 2', 'Internal Exam 2'),
        ('Class Test', 'Class Test'),
        ('Assignment', 'Assignment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField(default=100)
    assessment_type = models.CharField(max_length=255, choices=ASSESSMENT_CHOICES)  # Use choices here
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}/{self.max_marks}"