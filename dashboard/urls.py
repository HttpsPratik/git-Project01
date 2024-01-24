from os import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     
    path('', views.index),
    path('dashboard/home/', views.home, name="home"),
    

    #------For Email OTP------------#
    # path('signup/', views.signup),
    path("", views.index, name="index"),
    path("register", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login/", views.signin, name="signin"),
    # path('login/', views.login,name="login"),
    # # path('code/', views.code,name="code"),
    # path('logout/', views.logout,name="logout"),
    
    #---------For CRUD----------#
    path('dashboard/home',views.home),
    path('dashboard/add-adoption/',views.add_adoption),
    path('dashboard/delete-dashboard/<int:name>',views.delete_dashboard),
    path('dashboard/update-dashboard/<int:name>',views.update_dashboard),
    path('dashboard/do-update-dashboard/<int:name>',views.do_update_dashboard),
]
