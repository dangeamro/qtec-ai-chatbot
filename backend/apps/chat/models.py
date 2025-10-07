from django.db import models

class ChatSession(models.Model):
    """Represents a single conversation."""
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    """Stores each user and AI message."""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
