from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate_file(self, value):
        # Validate file type
        if not value.name.endswith('.txt'):
            raise ValidationError("Only .txt files are allowed.")
        
        # Validate file size (e.g., 5 MB limit)
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_file_size:
            raise ValidationError(f"File size cannot exceed {max_file_size / (1024 * 1024)} MB.")
        
        return value