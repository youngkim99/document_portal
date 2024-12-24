
# Create your models here.
from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255, default='Untitled Document')
    status = models.CharField(max_length=255, default='Pending')
    extracted_data = models.JSONField(null=True, blank=True)  # Store the extracted data
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name