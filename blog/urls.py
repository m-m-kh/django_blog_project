from django.urls import path
from . import views



urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('detail/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    # path('sendcomment/<int:pk>', views.SendComment.as_view(), name='send_comment')
]


