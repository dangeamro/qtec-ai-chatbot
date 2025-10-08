from django.urls import path
from .views import ChatView, SessionMessageView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
]