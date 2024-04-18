from django.http import HttpResponseForbidden
from django.conf import settings
from django.urls import reverse





class RestrictURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        restricted_urls = getattr(settings, 'RESTRICTED_URLS', [])
        current_path = request.path

        if current_path in restricted_urls:
            return HttpResponseForbidden("Access Forbidden")
        elif any(current_path.startswith(url) for url in restricted_urls):
            return HttpResponseForbidden("Access Forbidden")

        return None