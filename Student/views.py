from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponse
from django.contrib import messages
from django.utils import timezone
# Create your views here.
from adminapp.models import Teacher,Student,User,Department,Fee,Payment
from Teacher.models import Add_assignment,Attendance,InternalAssessmentMarks
from Student.models import *
from django.db.models import Count, Q,Sum

import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from reportlab.lib.pagesizes import landscape,A5
from reportlab.pdfgen import canvas
from django.utils import timezone
from reportlab.lib import colors

def studenthome(request):
    s =request.session.get('userid')
    user=User.objects.get(id=s)
    name=user.first_name +" "+ user.last_name 
    
    return render(request,'student/home.html',{'name':name})



def editstudprofile(request):
    s = request.session.get('userid')
    user = User.objects.get(id=s)
    student = Student.objects.get(student_id=user)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        address = request.POST['address']
        father_name = request.POST['father_name']
        mother_name = request.POST['mother_name']
        DOB = request.POST['DOB']
        username = request.POST['username']
        password = request.POST['password']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password: 
            user.set_password(password)
        user.save()
        student.phone_number = phone_number
        student.address = address
        student.father_name = father_name
        student.mother_name = mother_name
        student.DOB = DOB
        student.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('studenthome')

    context = {
        'user': user,
        'student': student,
        'dept': Department.objects.all(),
    }
    return render(request, 'student/editprofilestud.html', context)
def view_assignments(request):
    s = request.session.get('userid')
    user = User.objects.get(id=s)
    student = Student.objects.get(student_id=user)

    # Get assignments for the student's department and semester
    assignments = Add_assignment.objects.filter(
        subject__department_id=student.department_id,
        semester=student.semester
    )

    # Get submissions for the logged-in student
    submissions = Submission.objects.filter(student=student)
    submission_data = {submission.assignment_id: submission for submission in submissions}

    # Add marks and feedback to assignments
    for assignment in assignments:
        submission = submission_data.get(assignment.id)
        assignment.marks = submission.marks if submission else None
        assignment.feedback = submission.feedback if submission else None
        assignment.is_uploaded = submission is not None

    if request.method == "POST":
        assignment_id = request.POST.get('assignment_id')
        assignment = Add_assignment.objects.get(id=assignment_id)

        if assignment.due_date < timezone.now():
            messages.error(request, "You cannot upload after the deadline.")
            return redirect('viewassignment')

        file = request.FILES['file']
        Submission.objects.create(
            student=student,
            assignment=assignment,
            file=file
        )

        messages.success(request, "Assignment uploaded successfully.")
        return redirect('viewassignment')

    return render(request, 'student/viewassignment.html', {
        'assignments': assignments,
        'student': student,
        'now': timezone.now(),
    })


# views.py for studentapp

def student_marks_view(request):
    s = request.session.get('userid')
    user = User.objects.get(id=s)
    student = get_object_or_404(Student, student_id=user)

    # Fetch marks for the student
    marks = InternalAssessmentMarks.objects.filter(student=student).select_related('subject')

    return render(request, 'student/view_marks.html', {
        'marks': marks,
        'student': student,
    })



def view_internal_marks(request):
    s = request.session.get('userid')
    user = get_object_or_404(User, id=s)
    student = get_object_or_404(Student, student_id=user)
    marks = InternalAssessmentMarks.objects.filter(student=student).select_related('subject')

    return render(request, 'student/view_marks.html', {
        'marks': marks,
        'student': student,
    })


def view_attendance(request):
    s = request.session.get('userid')
    user = get_object_or_404(User, id=s)
    student = get_object_or_404(Student, student_id=user)

    # Fetch attendance records for the student
    attendance_records = Attendance.objects.filter(student=student).select_related('subject')

    return render(request, 'student/view_attendance.html', {
        'attendance_records': attendance_records,
        'student': student,
    })

def view_top_scorers(request):
    # Fetch all internal assessment marks and aggregate by student and semester
    top_scorers = (
        InternalAssessmentMarks.objects
        .values('student__department_id', 'student__semester', 'student__student_id__first_name', 'student__student_id__last_name')
        .annotate(total_marks=Sum('marks_obtained'))
        .order_by('student__semester', '-total_marks')
    )

    # Prepare a dictionary to hold top scorers for each semester
    top_scorers_by_semester = {}
    for scorer in top_scorers:
        semester = scorer['student__semester']
        if semester not in top_scorers_by_semester:
            top_scorers_by_semester[semester] = scorer
        else:
            # If the current scorer has more marks, update the top scorer for that semester
            if scorer['total_marks'] > top_scorers_by_semester[semester]['total_marks']:
                top_scorers_by_semester[semester] = scorer

    return render(request, 'student/view_top_scorers.html', {
        'top_scorers': top_scorers_by_semester,
    })


# views.py for studentapp

def view_dues(request):
    s = request.session.get('userid')
    user = get_object_or_404(User, id=s)
    student = get_object_or_404(Student, student_id=user)

    # Fetch fee status for the student
    fees = Fee.objects.filter(student=student)

    return render(request, 'student/view_fee_status.html', {
        'fees': fees,
        'student': student,
    })



def make_payment(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    # Log the fee details
    print(f"Making payment for Fee ID: {fee.id}, Student: {fee.student}")


    if fee.amount <= 0:
        return render(request, "student/payment_error.html", {"error": "Invalid fee amount."})

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount_in_paise = int(fee.amount * 100)  # Razorpay accepts amount in paise
    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": "1"  # Auto-capture payment
    }

    try:
        order = client.order.create(order_data)
    except Exception as e:
        return render(request, "student/payment_error.html", {"error": "Payment processing error."})

    return render(request, "student/make_payment.html", {
        "fee": fee,
        "order_id": order["id"],
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,
        "amount": fee.amount
    })




@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            response = json.loads(request.body)

            order_id = response.get('razorpay_order_id')
            pay_id = response.get('razorpay_payment_id')
            signature = response.get('razorpay_signature')
            fee_id = response.get('fee_id')

            print(f"Received fee_id: {fee_id}")
            print(f"Payment details: order_id={order_id}, pay_id={pay_id}, signature={signature}")

            if not all([order_id, pay_id, signature, fee_id]):
                return JsonResponse({"success": False, "error": "Incomplete payment details received."}, status=400)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': pay_id,
                'razorpay_signature': signature
            })

            # Retrieve fee object
            fee = get_object_or_404(Fee, id=fee_id)

            with transaction.atomic():
                fee.status = 'Paid'
                fee.save(update_fields=['status'])

                payment = Payment.objects.create(
                    fee=fee,
                    order_id=order_id,
                    pay_id=pay_id,
                    signature=signature,
                    amount_paid=fee.amount,
                    status='Paid'
                )

            return JsonResponse({"success": True, "pay_id": pay_id})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format."}, status=400)
        except Exception as e:
            print(f"Error processing payment: {e}")
            return JsonResponse({"success": False, "error": "Payment processing error."}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


    



# def generate_receipt(request, payment_id):
#     try:
#         # Fetch the payment and related fee & student
#         payment = get_object_or_404(Payment, id=payment_id)
#         fee = payment.fee  # Directly access the fee
#         student = fee.student  # Correct way to get the student

#         # Ensure the student object is correct
#         if not student:
#             return HttpResponse("Student not found.", status=404)

#         department = student.department_id.dept_name  # Ensure this is correct

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="receipt_{student.student_id.first_name}_{student.student_id.last_name}_{payment.id}.pdf"'

#         # Create a PDF object
#         p = canvas.Canvas(response, pagesize=landscape(A5))
#         width, height = landscape(A5)
#         margin_x = 50
#         start_y = height - 60

#         # **Title "CMS" (Centered)**
#         p.setFont("Helvetica-Bold", 24)
#         cms_text = "CMS"
#         cms_x = (width - p.stringWidth(cms_text, "Helvetica-Bold", 24)) / 2
#         p.drawString(cms_x, start_y, cms_text)

#         # **Random Address (Centered)**
#         start_y -= 30
#         p.setFont("Helvetica", 12)
#         address_text = "CMS Lane, Education City, EC 56789"
#         address_x = (width - p.stringWidth(address_text, "Helvetica", 12)) / 2
#         p.drawString(address_x, start_y, address_text)

#         # **Title "FEE PAYMENT RECEIPT" (Centered)**
#         start_y -= 30
#         p.setFont("Helvetica-Bold", 18)
#         title_text = "FEE PAYMENT RECEIPT"
#         title_x = (width - p.stringWidth(title_text, "Helvetica-Bold", 18)) / 2
#         p.drawString(title_x, start_y, title_text)

#         # **Line below title**
#         start_y -= 10
#         p.setStrokeColor(colors.black)
#         p.line(margin_x, start_y, width - margin_x, start_y)

#         # **Receipt Details (Left Aligned)**
#         start_y -= 20
#         p.setFont("Helvetica", 12)
#         details = [
#             f"Receipt ID: {payment.id}",
#             f"Student Name: {student.student_id.first_name} {student.student_id.last_name}",
#             f"Department: {department}",
#             f"Semester: {student.semester}"
#         ]

#         for detail in details:
#             p.drawString(margin_x, start_y, detail)
#             start_y -= 20

#         # **Payment Details Section**
#         start_y -= 30
#         p.setFont("Helvetica-Bold", 14)
#         p.drawString(margin_x, start_y, "Payment Details")

#         # **Table Header (Aligned)**
#         start_y -= 27
#         col1_x = margin_x
#         col2_x = width / 2 - 50
#         col3_x = width - margin_x - 150

#         p.setFont("Helvetica-Bold", 12)
#         p.setFillColor(colors.grey)
#         p.rect(margin_x, start_y, width - 2 * margin_x, 20, fill=1)
#         p.setFillColor(colors.black)

#         p.drawString(col1_x, start_y + 5, "Amount Paid")
#         p.drawString(col2_x, start_y + 5, "Payment Status")
#         p.drawString(col3_x, start_y + 5, "Payment Date")

#         # **Table Row (Aligned)**
#         start_y -= 20
#         p.setFont("Helvetica", 12)
#         p.drawString(col1_x, start_y, f"{payment.amount_paid:.2f}")
#         p.drawString(col2_x, start_y, payment.status)
#         p.drawString(col3_x, start_y, payment.created_at.strftime('%d-%m-%Y'))

#         # **Line below table**
#         start_y -= 10
#         p.line(margin_x, start_y, width - margin_x, start_y)

#         # **Footer (Centered)**
#         start_y -= 70
#         footer_text1 = "Thank you for your payment!"
#         footer_text2 = "For any queries, contact us at support@cms.com"

#         p.setFont("Helvetica-Oblique", 10)
#         footer_x1 = (width - p.stringWidth(footer_text1, "Helvetica-Oblique", 10)) / 2
#         p.drawString(footer_x1, start_y, footer_text1)

#         footer_x2 = (width - p.stringWidth(footer_text2, "Helvetica-Oblique", 10)) / 2
#         p.drawString(footer_x2, start_y - 20, footer_text2)

#         # Finalize the PDF
#         p.showPage()
#         p.save()

#         return response
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}", status=500)


def generate_receipt(request, payment_id):
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        fee = payment.fee
        student = fee.student

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'

        p = canvas.Canvas(response, pagesize=landscape(A5))
        width, height = landscape(A5)
        margin_x = 50
        start_y = height - 60

        # Title and Address
        p.setFont("Helvetica-Bold", 24)
        p.drawString((width - p.stringWidth("CMS", "Helvetica-Bold", 24)) / 2, start_y, "CMS")
        start_y -= 30
        p.setFont("Helvetica", 12)
        p.drawString((width - p.stringWidth("CMS Lane, Education City, EC 56789", "Helvetica", 12)) / 2, start_y, "CMS Lane, Education City, EC 56789")

        # Receipt Title
        start_y -= 30
        p.setFont("Helvetica-Bold", 18)
        p.drawString((width - p.stringWidth("FEE PAYMENT RECEIPT", "Helvetica-Bold", 18)) / 2, start_y, "FEE PAYMENT RECEIPT")
        start_y -= 10
        p.line(margin_x, start_y, width - margin_x, start_y)

        # Receipt Details
        start_y -= 20
        p.setFont("Helvetica", 12)
        details = [
            f"Receipt ID: {payment.id}",
            f"Student Name: {student.student_id.first_name} {student.student_id.last_name}",
            f"Department: {student.department_id.dept_name}",
            f"Semester: {student.semester}",
            f"Payment Status: {payment.status}",
            f"Receipt Generated On: {timezone.localtime(timezone.now()).strftime('%d-%m-%Y %H:%M:%S')}"
        ]

        for detail in details:
            p.drawString(margin_x, start_y, detail)
            start_y -= 20

        # Payment Details
        start_y -= 30
        p.setFont("Helvetica-Bold", 14)
        p.drawString(margin_x, start_y, "Payment Details")
        start_y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(margin_x, start_y, f"Amount Paid: {payment.amount_paid:.2f}")
        p.drawString(margin_x, start_y - 20, f"Payment Date: {payment.created_at.strftime('%d-%m-%Y')}")

        # Footer
        start_y -= 50
        p.setFont("Helvetica-Oblique", 10)
        p.drawString((width - p.stringWidth("Thank you for your payment!", "Helvetica-Oblique", 10)) / 2, start_y, "Thank you for your payment!")

        p.showPage()
        p.save()

        return response
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)