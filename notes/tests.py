from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="writer", email="writer@example.com", password="pass12345")
        self.other_user = User.objects.create_user(username="guest", email="guest@example.com", password="pass12345")
        self.note = Note.objects.create(
            owner=self.user,
            title="Sunday thoughts",
            content="A quiet afternoon with tea.",
        )
        self.other_note = Note.objects.create(
            owner=self.other_user,
            title="Someone else's page",
            content="Not for this journal.",
        )
        self.client.force_login(self.user)

    def test_note_list_and_search(self):
        response = self.client.get(reverse("notes:list"), {"q": "tea"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunday thoughts")
        self.assertNotContains(response, "Someone else's page")

    def test_create_note(self):
        response = self.client.post(
            reverse("notes:create"),
            {"title": "New page", "content": "A first line."},
        )

        created = Note.objects.get(title="New page")
        self.assertRedirects(response, reverse("notes:detail", kwargs={"pk": created.pk}))
        self.assertEqual(created.owner, self.user)

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
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
        self.assertTrue(Note.objects.filter(pk=self.other_note.pk).exists())

    def test_note_can_be_exported_as_pdf_or_image(self):
        pdf = self.client.get(reverse("notes:share-pdf", kwargs={"pk": self.note.pk}))
        image = self.client.get(reverse("notes:share-image", kwargs={"pk": self.note.pk}))

        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image["Content-Type"], "image/png")
        self.assertTrue(image.content.startswith(b"\x89PNG"))

    def test_other_users_notes_are_not_accessible(self):
        detail = self.client.get(reverse("notes:detail", kwargs={"pk": self.other_note.pk}))
        edit = self.client.get(reverse("notes:edit", kwargs={"pk": self.other_note.pk}))
        export = self.client.get(reverse("notes:share-pdf", kwargs={"pk": self.other_note.pk}))

        self.assertEqual(detail.status_code, 404)
        self.assertEqual(edit.status_code, 404)
        self.assertEqual(export.status_code, 404)

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(reverse("notes:list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response["Location"])

    def test_login_page_loads_before_google_credentials_are_added(self):
        self.client.logout()

        response = self.client.get(reverse("account_login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google SSO is wired in")
