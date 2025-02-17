from django.urls import path
from adminapp.views import *


urlpatterns=[
    path('',adminhome,name='adminhome'),
    path('admin_add_department/',admin_add_department,name='admin_add_department'),
    path('admin/view_department/',view_department,name='view_department'),
    path('admin_department_edit/<id>',admin_department_edit,name='admin_department_edit'),
    path('department_update/<id>',admin_department_update,name='admin_department_update'),
    path('admin_department_delete/<id>',admin_department_delete,name='admin_department_delete'),
    

    
    
    path('admin_add_subject',admin_add_subject,name='admin_add_subject'),    
    path('view_subject',view_subject,name='view_subject'),    
    path('admin_assign_teachers/<int:subject_id>',assign_teacher_to_subject,name='admin_assign_teachers'),    

        


    path('admin_add_teacher',admin_add_teacher,name='admin_add_teacher'),
    path('view_Teacher',view_Teacher,name='view_Teacher'),
    path('admin_Coordinator_delete/<int:id>/',delete_teacher,name='admin_Coordinator_delete'),

 path('view_students/',view_students,name='view_students'),
    path('view_verified_students/',view_verified_students,name='view_verified_students'),
    path('approve_stud/<int:id>/',approve_stud,name='approve_stud'),
    path('reject_stud/<int:id>/',reject_stud,name='reject_stud'),
    path('create_fee_due/', create_fee_due, name='create_fee_due'),
    path('view_fee_dues/', view_fee_dues, name='view_fee_dues'),
    

    ]