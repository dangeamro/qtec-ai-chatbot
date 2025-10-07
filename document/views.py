from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from .retriever import retriever

class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        with instance.file.open('r') as f:
            text = f.read()
        retriever.add_document(text)
