from django.db import models

class Document(models.Model):
    """Stores one uploaded .txt file."""
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
