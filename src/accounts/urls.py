from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('hi/', views.JWTAuthTestView.as_view(), name='jwt-auth-test'),
]
