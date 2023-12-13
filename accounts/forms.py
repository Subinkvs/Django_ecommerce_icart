from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import User
import re


class CustomUserForm(UserCreationForm):
    phonenumber = forms.CharField(max_length=15)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter confirmpassword'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter phonenumber'}))
    
   
    
    class  Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2','phonenumber']
       
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if len(username) < 3:
            raise forms.ValidationError("Given username is too short..please try again")
        return username
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
    
       
        if User.objects.filter(phonenumber=phonenumber).exists():
            raise forms.ValidationError("Given phone number already exists.")

        
        if not re.match(r'^\+91[0-9]{10}$', phonenumber):
            raise forms.ValidationError("Phone number must be in E.164 format:+91.")

        return phonenumber
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        char = '@'
        position = email.find(char)
        
        
        if char not in email:
            raise forms.ValidationError("Invalid address..")
        
        if position < 3:
            raise forms.ValidationError("Sorry, your email address is too short")
        

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Given email address already exists.")
        
        
        return email
        
 