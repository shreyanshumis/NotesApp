from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import NoteForm
from .models import Note
from .exports import build_note_image, build_note_pdf, note_filename


class NoteListView(ListView):
    model = Note
    context_object_name = "notes"
    template_name = "notes/note_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        notes = Note.objects.all()
        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Your note has been tucked safely into the journal.")
        return super().form_valid(form)


class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Your note has been updated.")
        return super().form_valid(form)


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:list")

    def form_valid(self, form):
        messages.success(self.request, "The note has been removed from your journal.")
        return super().form_valid(form)


def export_note_pdf(request, pk):
    note = get_object_or_404(Note, pk=pk)
    response = HttpResponse(build_note_pdf(note), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{note_filename(note, "pdf")}"'
    return response


def export_note_image(request, pk):
    note = get_object_or_404(Note, pk=pk)
    response = HttpResponse(build_note_image(note), content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="{note_filename(note, "png")}"'
    return response
