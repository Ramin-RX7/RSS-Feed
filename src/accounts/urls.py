from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/refresh/', views.RefreshToken.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('hi/', views.JWTAuthTestView.as_view(), name='jwt-auth-test'),
]
