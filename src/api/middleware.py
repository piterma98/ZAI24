from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.urls import reverse


class CustomSessionMiddleware(SessionMiddleware):
    """Custom session middleware that disables authenticating via session id in graphql view."""

    def process_request(self, request) -> None:
        if reverse("user-graphql") in request.build_absolute_uri():
            request.session = {}
            return
        super().process_request(request)

    def process_response(self, request, response) -> HttpResponse:
        if reverse("user-graphql") in request.build_absolute_uri():
            return response
        return super().process_response(request, response)
