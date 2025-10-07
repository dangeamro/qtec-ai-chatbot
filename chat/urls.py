from django.urls import path
from .views import ChatView, SessionMessageView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('session/<int:id>/messages/', SessionMessageView.as_view(), name='session-messages'),
]