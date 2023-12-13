from .decorator import user_not_authenticated
from .forms import UserCreationForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.forms import  CustomUserForm
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout, get_user_model
from product.models import MenClothing,BannerImage,Cart,Wishlist
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import token_generator
from django.views import View
from product.models import BannerImage
 
# To activate a new user account using email confirmation
class activate(View):
    '''To activate a new user account using email confirmation '''
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Thank you for your email confirmation. Now you can log in to your account.")
            return redirect('loginpage')
        else:
            messages.error(request, 'Activation link is invalid')
        return redirect('index')

# To verify a new user account after user register with email confirmation
class activateEmail(View):
    '''To verify a new user account after user register with email confirmation '''
    def send_activation_email(self, request, user, to_email):
        mail_subject = "Activate your user account."

        message = render_to_string("template_activate_account.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })

        email = EmailMessage(mail_subject, message, to=[to_email])

        if email.send():
            messages.success(request, f'Dear {user}, please go to your email {to_email} inbox and click on \
                the received activation link to confirm and complete the registration. Note: Check your spam folder.')
        else:
            messages.success(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# To render the landing page of the project
class home(View):
    template_name = 'index.html'
    '''To render the landing page of the project '''
    def get_context_data(self,request):
        prods = MenClothing.objects.filter(is_featured=True)
        bannerimage = BannerImage.objects.all()
        cartitem = Cart.objects.filter(user=self.request.user.id)
        total_quantity = sum(item.product_qty for item in cartitem)
        wishlist = Wishlist.objects.filter(user=request.user.id)
        total_item =len(wishlist)
        
        context = {
            'prods': prods,
            'bannerimage': bannerimage,
            'cartitem': cartitem,
            'total_quantity': total_quantity,
             'total_item':total_item
        }

        return context

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    

# signup page for user registeration with validation
class signuppage(View):
    template_name = 'register.html'
    '''signup page for user registeration with validation'''
    def get(self, request):
        form = CustomUserForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateemail = activateEmail()
            activateemail.send_activation_email(request, user, form.cleaned_data['email'])
            return redirect('index')

        context = {'form': form}
        return render(request, self.template_name, context)

# loginpage for the user     
class loginpage(View):
    template_name = 'signin.html'
    '''loginpage for the user '''
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('/')
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('/')
        else:
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request, username=name, password=passwd)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                prods = MenClothing.objects.all()
                bannerimage = BannerImage.objects.all()
                return render(request, 'index.html', {'prods': prods, 'bannerimage': bannerimage})
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect('loginpage') 
        
     
# logout button for the user
class logoutpage(View):
    '''logout button for the user'''
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Logout Successfully")
        return redirect('/')





