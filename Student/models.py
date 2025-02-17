from django.db import models
from adminapp.models import Student, Subject
from Teacher.models import Add_assignment

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Add_assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    feedback = models.TextField(null=True, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'assignment')

