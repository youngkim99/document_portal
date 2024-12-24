import os
from .models import Document
from pathlib import Path
from .extract import process_pdf  # The script provided earlier
import json

sample_extracted_data = {
  "bill_of_lading_number": {
    "value": "BOL123456",
    "confidence": 0.95
  },
  "invoice_number": {
    "value": "INV-98765",
    "confidence": 0.92
    }
}


def handle_uploaded_document(document_id):
    document = Document.objects.get(id=document_id)
    pdf_path = document.file.path
    try:
        # Process the PDF
        # This is what hasn't worked
        # extracted_data = process_pdf(pdf_path)
        
        # Update the document instance with extracted data
        document.extracted_data = sample_extracted_data

        # PLACEHOLDER FOR EXTRACTED DATA
        document.status = "Processed"
    except Exception as e:
        print(f"Error processing document {document_id}: {e}")
        document.status = "Error"

    
    # Save the updated document
    document.extracted_data = sample_extracted_data

    document.save()
    print("WORKING")
