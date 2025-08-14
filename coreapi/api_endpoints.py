from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
# from app.accounts.views import account_management_view as user_views
from app.accounts.views import account_management_view as user_views
from app.accounts.views import profile_management_view as profile_views
from app.accounts.views import password_management_view as password_views
from app.dashboard import views as admin_views
from app.subscribtions import views as subscriptions_view
from app.stripe import views as stripe_view
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
    path("user-subscriptions-list/",subscriptions_view.ActiveSubscriptionListView.as_view(),name="user_subscription_list"),
    path("admin-subscriptions-list/",subscriptions_view.SubscriptionListCreateView.as_view(),name="admin_subscription_list_create"),
    path("admin-subscriptions-list/",subscriptions_view.SubscriptionPartialUpdateView.as_view(),name="admin_subscription_update"),
    # 
    path("subscription/purchase/",stripe_view.CreateStripeCheckoutSessionView.as_view(),name="purchase-a-plan"),
    path("subscription/cancel/", stripe_view.CancelSubscriptionView.as_view(), name="cancel_running_subscription"),
    path("stripe/webhook/",stripe_view.stripe_webhook,name="webhook from stripe"),
    # 
    path("contact-us/",admin_views.contact_us,name="contact-us+help-and-support"),
    path('privacy-policy/', admin_views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', admin_views.TermsConditionsView.as_view(), name='terms-and-conditions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
