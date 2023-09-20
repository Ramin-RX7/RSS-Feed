from django.urls import path

from .views import *


urlpatterns = [
    path("like/", LikeView.as_view(), name="like"),
    path("comment/", CommentCreateView.as_view(), name="comment"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
]
