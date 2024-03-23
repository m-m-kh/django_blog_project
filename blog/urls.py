from django.urls import path
from . import views



urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('detail/<str:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('edit/<str:slug>', views.PostEditView.as_view(), name='post_edit'),
    path('delete/<str:slug>', views.PostDeleteView.as_view(), name='post_delete'),
    # path('sendcomment/<int:pk>', views.SendComment.as_view(), name='send_comment')
]


