from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',home.as_view(), name="index"),
    path('register.html',signuppage.as_view(), name="signuppage"),
    path('signin.html', loginpage.as_view(), name ="loginpage"),
    path('logout/', logoutpage.as_view(), name = "logoutpage"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name = "password_reset_complete"),
    path('activate/<uidb64>/<token>', activate.as_view(), name='activate')
    
]