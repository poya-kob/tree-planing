import re
from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            for pattern in settings.LOGIN_REQUIRED_URLS:
                if re.match(pattern, request.path):
                    return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return self.get_response(request)
