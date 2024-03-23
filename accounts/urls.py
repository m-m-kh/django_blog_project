from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/confirm/', views.SignUpConfirm.as_view(), name='signup_confirm'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    # path('signup/', , name='signup')
]