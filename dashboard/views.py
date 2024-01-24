from multiprocessing import context
from django.shortcuts import render,redirect
from .forms import RegisterForm
from .models import OtpToken

import dashboard
from .models import Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout,get_user_model


def index(request):
    return render(request, 'index.html')



#-------For Email OTP--------#

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "signup.html", context)




def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        
        if user_otp.otp_code == request.POST.get('otp_code', ''):
            
            
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! Processed Login.")
                return redirect("signin")
            
           
            else:
                messages.warning(request, "The OTP has expired, get a new OTP ??")
                return redirect("verify-email", username=user.username)
        
        
        
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)




def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
          
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "Pratik.thapa.1223@gmail.com"
            receiver = [user.email, ]
        
        
            
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "Enter your email-address again to get OTP")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "resend_otp.html", context)




def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("home")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "login.html")
    
    

# def login(request):
    
#     return render(request, 'dashboard/login.html')
# def code(request):
    
#     return render(request, 'dashboard/code.html')

# def logout(request):
    
#     pass




#---------For CRUD---------------#
def home(request):
    dashboard = Comment.objects.all()
    context= {'dashboard':dashboard}
    return render(request, 'dashboard/home.html', context)#{'dashboard':dashboard}

def add_adoption(request):
  if request.method=='POST':
    print ("Added")
    dashboard_email =  request.POST.get("dashboard_email")
    dashboard_title =  request.POST.get("dashboard_title")
    dashboard_description = request.POST.get("dashboard_description")
    dashboard_image = request.POST.get("dashboard_image")


    s = Comment()
    s.email = dashboard_email
    s.title = dashboard_title
    s.description = dashboard_description
    s.image = dashboard_image
    
    s.save()
    return redirect("home")
  

  return render(request, 'dashboard/add_adoption.html')

def delete_dashboard(request,name):
   s=Comment.objects.get(pk=name)
   s.delete()

   return redirect("/dashboard/home/")
  
def update_dashboard(request, name):
   dashboard=Comment.objects.get(pk=name)
   return render(request,"dashboard/update_adoption.html",{'dashboard/home':dashboard})

def do_update_dashboard(request, name):
    dashboard_email =  request.POST.get("dashboard_email")
    dashboard_title =  request.POST.get("dashboard_title")
    dashboard_description = request.POST.get("dashboard_description")
    dashboard_image = request.POST.get("dashboard_image")

    dashboard=Comment.objects.get(pk=name)
    dashboard.email = dashboard_email
    dashboard.title = dashboard_title
    dashboard.description = dashboard_description
    dashboard.image = dashboard_image
    
    dashboard.save()
    return redirect("/dashboard/home/")
