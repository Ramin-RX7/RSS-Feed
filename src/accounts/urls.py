from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePassword.as_view(), name="change_password"),
    path('reset-password/<str:code>', views.ResetPassword.as_view({"get":"get", "post":"post"}), name="reset_password"),
    path('reset-password/', views.ResetPassword.as_view({"post":"reset_password_request"}), name="reset_password_request"),
]
