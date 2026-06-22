from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.NoteListView.as_view(), name="list"),
    path("notes/new/", views.NoteCreateView.as_view(), name="create"),
    path("notes/<int:pk>/", views.NoteDetailView.as_view(), name="detail"),
    path("notes/<int:pk>/edit/", views.NoteUpdateView.as_view(), name="edit"),
    path("notes/<int:pk>/delete/", views.NoteDeleteView.as_view(), name="delete"),
    path("notes/<int:pk>/share/pdf/", views.export_note_pdf, name="share-pdf"),
    path("notes/<int:pk>/share/image/", views.export_note_image, name="share-image"),
]
