from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteViewsTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Sunday thoughts", content="A quiet afternoon with tea.")

    def test_note_list_and_search(self):
        response = self.client.get(reverse("notes:list"), {"q": "tea"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunday thoughts")

    def test_create_note(self):
        response = self.client.post(
            reverse("notes:create"),
            {"title": "New page", "content": "A first line."},
        )

        self.assertRedirects(response, reverse("notes:detail", kwargs={"pk": 2}))
        self.assertTrue(Note.objects.filter(title="New page").exists())

    def test_update_and_delete_note(self):
        response = self.client.post(
            reverse("notes:edit", kwargs={"pk": self.note.pk}),
            {"title": "Sunday revised", "content": "Still a quiet afternoon."},
        )
        self.assertRedirects(response, self.note.get_absolute_url())
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Sunday revised")

        response = self.client.post(reverse("notes:delete", kwargs={"pk": self.note.pk}))
        self.assertRedirects(response, reverse("notes:list"))
        self.assertFalse(Note.objects.exists())

    def test_note_can_be_exported_as_pdf_or_image(self):
        pdf = self.client.get(reverse("notes:share-pdf", kwargs={"pk": self.note.pk}))
        image = self.client.get(reverse("notes:share-image", kwargs={"pk": self.note.pk}))

        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image["Content-Type"], "image/png")
        self.assertTrue(image.content.startswith(b"\x89PNG"))
