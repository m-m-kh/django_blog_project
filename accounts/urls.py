from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/confirm/', views.GoogleSignUpConfirm.as_view(), name='google_signup_confirm'),
    path('signup/set_password/', views.GoogleSetPass.as_view(), name='google_set_pass'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('confirm_email/<uuid>/<token>/', views.ConfirmEmail.as_view(),name='confirm_email')
    # path('confirm_email/', views.ConfirmEmail.as_view(),name='confirm_email')
    # path('signup/', , name='signup')
]