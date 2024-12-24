from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .models import Document
import json
from .serializers import DocumentSerializer
from .utils import handle_uploaded_document

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)
        
        # Save the file in the database
        doc = Document.objects.create(file=file)
        
        # Process the document
        handle_uploaded_document(doc.id)
        
        #hardcoded for now
        doc.extracted_data = {
            "bill_of_lading_number": {
                "value": "BOL123456",
                "confidence": 0.95
            },
            "invoice_number": {
                "value": "INV-98765",
                "confidence": 0.92
            }
        }
        doc.status = "Processed"

        data = {
                "id": doc.id,
                "name": doc.name,
                "file": doc.file.url,
                "uploaded_at": doc.uploaded_at,
                "status": doc.status,
                "extracted_data": doc.extracted_data,
            }
        print(data)
        return Response(data)

class DocumentListView(APIView):
    def get(self, request, *args, **kwargs):
        documents = Document.objects.all()
        data = [
            {
                "id": doc.id,
                "name": doc.name,
                "file": doc.file.url,
                "uploaded_at": doc.uploaded_at,
                "status": doc.status,
                "extracted_data": doc.extracted_data,
            }
            for doc in documents
        ]
        return JsonResponse(data, safe=False)


class DocumentDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            doc = Document.objects.get(pk=pk)
            data = {
                "id": doc.id,
                "name": doc.name,
                "file": doc.file.url,
                "uploaded_at": doc.uploaded_at,
                "status": doc.status,
                "extracted_data": doc.extracted_data,
            }
            return Response(data)
        except Document.DoesNotExist:
            return JsonResponse({"error": "Document not found"}, status=404)

# Create your views here.
