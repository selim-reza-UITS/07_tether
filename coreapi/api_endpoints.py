from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
# from app.accounts.views import account_management_view as user_views
from app.accounts.views import account_management_view as user_views
from app.accounts.views import profile_management_view as profile_views
from app.accounts.views import password_management_view as password_views
from app.dashboard import views as admin_views
urlpatterns = [
    # your existing URLs
    path("sign-up/",user_views.UserSignupView.as_view()),
    path("login/",user_views.LoginView.as_view()),
    path('profile/', profile_views.ProfileView.as_view()),
    # otp:
    path("send-otp/",password_views.RequestOTPView.as_view()),
    path("verify-otp/",password_views.VerifyOTPView.as_view()),
    path("reset-password/",password_views.ResetPasswordView.as_view()),
    path("update-password/",password_views.ChangePasswordView.as_view()),
    # 
    path('privacy-policy/', admin_views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', admin_views.TermsConditionsView.as_view(), name='terms-and-conditions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
