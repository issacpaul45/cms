from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponse
from django.contrib import messages
from adminapp.models import *
from django.http import JsonResponse



def adminhome(request):
   
    return render(request,'admin/home.html')


def admin_add_department(request):
    if request.method=="GET":
        return render(request,'admin/add_department.html')
    else:
        dept=Department()
        dept.dept_name=request.POST.get('dept_name')   
        
        dept.save()
      
        return HttpResponse("<script>window.alert('Successfully Department Added!!');window.location.href='/adminapp/admin_add_department/'</script>")

def view_department(request):
    
    dept=Department.objects.all()
    return render(request,'admin/view_department.html',{'data':dept})

def admin_department_delete(request,id):
    dept = Department.objects.get(id=id)  
    dept.delete()  
    return redirect("view_department") 


def admin_department_edit(request,id):
    dept = Department.objects.get(id=id)  
    return render(request,'admin/edit_department.html', {'dept':dept})  

def admin_department_update(request, id):    
        dept = Department.objects.get(id=id)  
        dept.dept_name=request.POST.get('dept_name')
       
        dept.save()
        
        return redirect("view_department")     



def admin_add_teacher(request):
    if request.method=="GET":
        x=Department.objects.all()
        return render(request,'admin/add_teacher.html',{'dept':x})      
    else:
        department=request.POST['dept_id']
        department_id = Department.objects.get(id=department)       
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        address=request.POST['address']
        phone=request.POST['phone']
        salary=request.POST['salary']
        experience=request.POST['experience']
        username=request.POST['username']
        password=request.POST['password']    
        new_user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,
                                          password=password,usertype='teacher')
        new_user.save()   
        tech=Teacher.objects.create(teacher_id=new_user,department_id=department_id,
                                    address=address,phone_number=phone,
                                   salary=salary,experience=experience )
        tech.save()
        return HttpResponse("<script>window.alert('Successfully Teacher Details Added!!');window.location.href='/adminapp/admin_add_teacher'</script>")


def view_Teacher(request):    
    details = Teacher.objects.select_related('teacher_id','department_id')
    return render(request,'admin/view_Teacher.html',{'data':details})

def delete_teacher(request, id):
    details = User.objects.get(id=id)
    details.delete()
    return redirect('view_Teacher')

def admin_add_subject(request):
    if request.method=="GET":
        x=Department.objects.all()
        return render(request,'admin/add_subject.html',{'dept':x})  
    else:
        department=request.POST['dept_id']
        department_id = Department.objects.get(id=department)
        sem= request.POST['sem']       
        subj= request.POST['subname']    
        sub=Subject.objects.create(department_id=department_id,semester=sem,
                                    subject=subj)
        sub.save()        
        return HttpResponse("<script>window.alert('Successfully Subject Added!!');window.location.href='/adminapp/view_subject'</script>")  

        
def view_students(request):
    data=Student.objects.filter(student_id__is_active=False)  
    return render(request,'admin/view_Students_for_Varify.html',{'data':data})


def view_subject(request):
    subjects = Subject.objects.select_related('department_id').all().order_by('department_id', 'semester')
    return render(request, 'admin/viewsubject.html', {'subjects': subjects})

def assign_teacher_to_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    teachers = Teacher.objects.filter(department_id=subject.department_id)
    
    # Get the already assigned teacher, if exists
    assigned_teacher_subject = TeacherSubject.objects.filter(subject=subject).first()
    assigned_teacher = assigned_teacher_subject.teacher if assigned_teacher_subject else None

    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        teacher = Teacher.objects.get(id=teacher_id)

        # Check if a teacher is already assigned to this subject
        if assigned_teacher_subject:
            messages.warning(request, f'This subject is already assigned to {assigned_teacher.teacher_id.first_name} {assigned_teacher.teacher_id.last_name}.')
            return redirect('admin_assign_teachers', subject_id=subject_id)

        # Assign new teacher
        TeacherSubject.objects.create(teacher=teacher, subject=subject)
        messages.success(request, f'Teacher {teacher.teacher_id.first_name} {teacher.teacher_id.last_name} assigned successfully.')
        return redirect('admin_assign_teachers', subject_id=subject_id)

    return render(request, 'admin/assign_teacher_to_subject.html', {
        'subject': subject,
        'teachers': teachers,
        'assigned_teacher': assigned_teacher
    })

def view_verified_students(request):
    data=Student.objects.filter(student_id__is_active=True)  
    return render(request,'admin/view_Students.html',{'data':data})

    
def approve_stud(request,id):
    std=User.objects.get(id=id)
    std.is_active=True
    std.save()
    return HttpResponse("<script>window.alert('Student Approved Successfully !!');window.location.href='/adminapp/view_students/'</script>")    


def reject_stud(request,id):
    std=User.objects.get(id=id)
    std.is_active= False
    std.save()
    return HttpResponse("<script>window.alert('Student Rejected Successfully !!');window.location.href='/adminapp/view_students/'</script>")    





def create_fee_due(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')

        # Ensure fees are created for all students who don't have a pending fee
        students = Student.objects.all()
        fees_created = 0

        for student in students:
            if not Fee.objects.filter(student=student, status='Pending').exists():
                Fee.objects.create(
                    student=student,
                    amount=amount,
                    due_date=due_date,
                    status='Pending'
                )
                fees_created += 1

        messages.success(request, f"Fee due created for {fees_created} students!")
        return redirect('view_fee_dues')  # Redirect to the fee list page

    students = Student.objects.all()
    return render(request, 'admin/create_fee_due.html', {'students': students})

def view_fee_dues(request):
    fees = Fee.objects.all()
    return render(request, 'admin/view_fee_dues.html', {
        'fees': fees,
    })
