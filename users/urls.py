from django.urls import path,include

from .views import (
    CustomSignUpView,
    CustomLoginView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    EditUserProfileView,
    ViewUserProfileView,
)

from django.contrib.auth import views as auth_views

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .api_views import RegisterView, LoginView, ProfileView, PasswordResetView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



app_name = 'users'  # Define the namespace for your app

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('edit-user-profile/', EditUserProfileView.as_view(), name='edit-user-profile'),
    path('user-profile/', ViewUserProfileView.as_view(), name='view-user-profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('api/signup/', RegisterView.as_view(), name='api-signup'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/user-profile/', ProfileView.as_view(), name='api-profile'),
    path('api/password-reset/', PasswordResetView.as_view(), name='api-password-reset'),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]