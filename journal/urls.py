import os

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "commit": os.environ.get("RENDER_GIT_COMMIT", "local")[:7],
        }
    )


urlpatterns = [
    path("healthz/", health_check, name="health-check"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("notes.urls")),
]
