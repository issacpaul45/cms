from django.urls import path
from .views import *


urlpatterns=[
    path('',home,name='home'),
    # path('UserSignUp/',UserSignUp,name='USignUp'),
    # path('ShopSignUp/',ShopSignUp,name='ShopSignUp'),
    path('SignIn/',SignIn,name='SignIn'),
    path('accounts_logout/',accounts_logout,name='accounts_logout'),
    path('student_reg/',student_reg,name='student_reg'),
    
]