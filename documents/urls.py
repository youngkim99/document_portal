from django.urls import path
from .views import DocumentUploadView, DocumentDetailView, DocumentListView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('', DocumentListView.as_view(), name='document-list'),
]
