from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Give this page a title…"}),
            "content": forms.Textarea(attrs={"placeholder": "Begin writing your thoughts…", "rows": 12}),
        }
