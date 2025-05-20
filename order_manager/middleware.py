from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings


class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Public pages
        self.public_paths = [
            "/",
            "/driver/logout/",
            "/driver/login/",
            "/driver/login/create/",
            "/driver/register/",
            "/driver/register/create/"
        ]

        # Pages allowed for users
        self.users_allowed_paths = [
            "/tracker/tracking/",
            "/tracker/delivery-choice/",
            "/tracker/get-host/",
            "/orders/order-in-progress/",
            "/tracker/update-location/",
            "/orders/update/status/",
            "/orders/open/",
            "/orders/choice/",
        ]

    def __call__(self, request):
        login_url = reverse("driver:login")

        if request.path in self.public_paths or request.path == login_url:
            return self.get_response(request)

        if not request.user.is_superuser and request.path not in self.users_allowed_paths:
            # print("Redirecionando", request.path)
            # return render(request, "global/home.html", context={"message": "Você tentou acessar uma página restrita!"})
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
