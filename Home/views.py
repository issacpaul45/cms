from django.shortcuts import  render,redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from adminapp.models import Teacher,Student,User,Department




def home(request):
   
    return render(request,'Home/home.html')


def SignIn(request):
    
    if request.method == 'GET':
        context = {}
        context['form'] = ''
        return render(request,'Home/SignIn.html',context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user,'///////////')
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect("adminhome")
            else:
                if user.usertype == 'student': # user
                    if user.is_active==1:
                        request.session["userid"]=user.id
                        
                        return redirect("studenthome")
                    else:
                        return HttpResponse("<script>window.alert('Student is no Yet Varified!');window.location.href='/SignIn/'</script>")
                elif user.usertype == "teacher": # Teacher
                        login(request,user)
                        request.session['teach_id']=user.id                         
                        return redirect("teacherhome")
                elif user.usertype == "Exam_Controller": # Exam_Controller
                        login(request,user)
                        request.session['Exam_Controller_id']=user.id                         
                        return redirect("examControllerhome")
                elif user.usertype == "Office_Staff": # Office_Staff
                        login(request,user)
                        request.session['Office_Staff_id']=user.id                         
                        return redirect("staffhome")
                else:
                    print('................')
                    return HttpResponse("<script>window.alert('Invalid!');window.location.href='/SignIn/'</script>")
               
        else:
            return HttpResponse("<script>window.alert('Invalid Credentials!');window.location.href='/SignIn/'</script>")
        
   
    return render(request,'Home/SignIn.html')


def accounts_logout(request):
    logout(request)
    return redirect('SignIn')    


def student_reg(request):
  
    if request.method=="GET":
        x=Department.objects.all()
        return render(request,'Home/add_student.html',{'dept':x})      
    else:
        department=request.POST['dept_id']
        department_id = Department.objects.get(id=department)
        sem= request.POST['sem']
        
        
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        address=request.POST['address']
        phone=request.POST['phone']
        father_name=request.POST['father_name']
        mother_name=request.POST['mother_name']
        sslc=request.POST['sscl']
        plus_two=request.POST['plus_two']
        DOB=request.POST['DOB']
        photo=request.FILES['photo']
       
        username=request.POST['username']
        password=request.POST['password']
        
        
        new_user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,
                                          password=password,usertype='student',is_active=0)
        new_user.save()
        
        stud=Student.objects.create(student_id=new_user,department_id=department_id, semester=sem,
                                    father_name=father_name,mother_name=mother_name,address=address,phone_number=phone,
                                   DOB=DOB,sslc=sslc,plus_two=plus_two,photo=photo )
        stud.save()


        return HttpResponse("<script>window.alert('Successfully Student Registered!!');window.location.href='/SignIn/'</script>")


 

