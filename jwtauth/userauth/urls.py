from django.contrib import admin
from django.urls import path, include
from .views import Register, LoginView, SellerView, BuyerView, ChangePasswordView, FindAccount, OtpView, ForgetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', LoginView.as_view()),
    path('seller/', SellerView.as_view()),
    path('buyer/', BuyerView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('findaccount/', FindAccount.as_view()),
    path('otpverify/', OtpView.as_view()),
    path('forgetpass/', ForgetPasswordView.as_view()),

]
