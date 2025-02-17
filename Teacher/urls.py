from django.urls import path
from Teacher.views import *


urlpatterns=[
   path('',teacherhome,name='teacherhome'),
   path('editprofileteacher',editteachprofile,name='editprofileteacher'),
   path('viewteachersubject',view_subjects,name='viewteachersubject'),
   path('addassignment',create_assignment,name='addassignment'),
   path('view_all_assignments',teacher_assignments,name='view_all_assignments'),
   path('view_submissions/<int:assignment_id>/', view_submissions, name='view_submissions'),
   path('review_submission/<int:submission_id>/', review_submission, name='review_submission'),
   path('view_attnd', view_attendance, name='view_attnd'),
   path('record_marks', record_marks, name='record_marks'),
   path('view_student_marks',view_student_marks, name='view_student_marks'),
   path('generate_student_record',generate_student_record, name='generate_student_record'),

   ]