from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    """
    Middleware para restringir o acesso de diferentes tipos de usuários às páginas corretas.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            "/driver/login/", "/driver/register/", "/driver/register/create/", "/orders/"]
        self.motorista_allowed_paths = ["/tracker/tracking/"]
        self.admin_allowed_paths = [
            "/admin/", "/dashboard/", "/orders/", "/orders/register/"]

    def __call__(self, request):
        login_url = reverse("driver:login")

        # Permitir acesso às páginas públicas
        if request.path in self.public_paths or request.path == login_url:
            return self.get_response(request)

        # Verifica autenticação pela sessão
        user_id = request.session.get("user_id")
        user_type = request.session.get("user_type")  # "driver", "admin", etc.

        if not user_id:
            # Se não estiver autenticado, redireciona
            return redirect(login_url)

        # Motorista comum tem acesso restrito
        if user_type == "driver" and request.path not in self.motorista_allowed_paths:
            return redirect("tracker:tracking")

        # Admin tem acesso livre a tudo dentro de /admin/
        if user_type == "admin":
            if request.path.startswith("/admin/") or request.path in self.admin_allowed_paths:
                return self.get_response(request)
            return redirect("admin_dashboard")

        return self.get_response(request)
