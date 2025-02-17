from django.db import models
from django. contrib. auth.models import AbstractUser
# Create your models here.
class Department(models.Model):
    dept_name=models.CharField(max_length=30)

class User(AbstractUser):
    usertype = models.CharField(max_length=50)    


class Subject(models.Model):
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    semester=models.CharField(max_length=30)
    subject=models.CharField(max_length=30)
    
class Student(models.Model):
    student_id=models.ForeignKey(User, on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    semester=models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    father_name=models.CharField(max_length=30)    
    mother_name=models.CharField(max_length=30)    
    DOB=models.DateField()
    sslc=models.IntegerField()
    plus_two=models.IntegerField()    
    photo = models.ImageField(
        upload_to='images/')
  


class Teacher(models.Model):
    teacher_id=models.ForeignKey(User, on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)    
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    salary=models.IntegerField()
    experience=models.IntegerField()        



class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)



class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"


class Payment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    pay_id = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.fee.student}"
    



    