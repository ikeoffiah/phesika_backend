from django.urls import path
from .views import LandingPageView, CompleteSignUpView, VerifyEmail, ReferralLandingView, Customerdetails, PasswordTokenCheckView, SetNewPasswordView,ResetPasswordView,LoginView, ContactUsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
TokenVerifyView
)

urlpatterns = [
    path('', LandingPageView.as_view(),name='landing'),
    path('activate_user/<uidb64>/<token>', VerifyEmail.as_view(), name='activate'),
    path('complete_signup', CompleteSignUpView.as_view(), name='complete-signup'),
    path('login', LoginView.as_view(), name='login'),
    path('referral', ReferralLandingView.as_view(), name='referral'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_detail', Customerdetails.as_view(), name='get_detail'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password_reset_confirm/<uidb64>/<token>', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordView.as_view(), name='password-reset-complete'),
    path('password-reset', ResetPasswordView.as_view(), name='password-reset'),
    path('contact_us', ContactUsView.as_view(), name='contact_us')
]

