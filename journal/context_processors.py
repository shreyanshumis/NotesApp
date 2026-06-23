from django.conf import settings


def google_sso_status(request):
    configured = bool(
        getattr(settings, "GOOGLE_OAUTH_CLIENT_ID", "")
        and getattr(settings, "GOOGLE_OAUTH_CLIENT_SECRET", "")
    )

    if not configured:
        try:
            from allauth.socialaccount.models import SocialApp

            configured = SocialApp.objects.filter(provider="google").exists()
        except Exception:
            configured = False

    return {"google_sso_configured": configured}
