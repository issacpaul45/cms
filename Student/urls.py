from django.urls import path
from Student.views import *


urlpatterns=[
    path('',studenthome,name='studenthome'),
    path('editstudprofile',editstudprofile,name='editstudprofile'),
    path('viewassignment',view_assignments,name='viewassignment'),
    path('view_marks',view_internal_marks,name='view_marks'),
    path('view_attendance',view_attendance,name='view_attendance'),
    path('view_top_scorers', view_top_scorers, name='view_top_scorers'),
    path('view_fee_status', view_dues, name='view_fee_status'),  
    path('make_payment/<int:fee_id>/', make_payment, name='make_payment'),
    path("payment_callback", payment_callback, name="payment_callback"),
    path('generate_receipt/<int:payment_id>/', generate_receipt, name='generate_receipt'),
]