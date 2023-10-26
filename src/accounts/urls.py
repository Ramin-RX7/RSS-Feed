from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),

    path('change-password/', views.ChangePassword.as_view(), name="change_password"),
    path('reset-password/<str:code>/', views.ResetPassword.as_view({"get":"get", "post":"post"}), name="reset_password"),
    path('reset-password/', views.ResetPassword.as_view({"post":"reset_password_request"}), name="reset_password_request"),

    path('active-sessions/', views.ActiveSessionsView.as_view({"get":"get"}), name="active_sessions"),

    path('logout/', views.LogoutView.as_view(), name='logout_current'),
    path('logout/others/', views.ActiveSessionsView.as_view({"get":"logout_others"}), name="logout_others"),
    path('logout/all/', views.ActiveSessionsView.as_view({"get":"logout_all"}), name="logout_all"),
    path('logout/<str:session_code>/', views.ActiveSessionsView.as_view({"get":"logout"}), name="logout_other"),

    path('profile/<str:username>/', views.ProfileView.as_view({"get":"get"})),
    path('profile/<str:username>/likes/', views.ProfileView.as_view({"get":"likes"})),
    path('profile/<str:username>/subscriptions/', views.ProfileView.as_view({"get":"subscriptions"})),
    path('profile/<str:username>/recommendations/', views.ProfileView.as_view({"get":"likes"})),
]
