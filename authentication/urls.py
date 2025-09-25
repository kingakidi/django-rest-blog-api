from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='user-signup'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
