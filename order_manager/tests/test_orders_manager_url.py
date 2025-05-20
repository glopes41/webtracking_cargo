from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class OrdersTest(TestCase):
    def setUp(self):
        # Cria um superusuário
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )

        # Cria um usuário comum
        self.normal_user = User.objects.create_user(
            username='teste',
            password='senha123'
        )

    def test_order_manager_orders_url_is_correct(self):
        url = reverse('order_manager:orders')
        self.assertEqual(url, '/orders/')

    def test_orders_manager_orders_url_accessible_by_name(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('order_manager:orders'))
        self.assertEqual(response.status_code, 200)

    def test_orders_manager_orders_url_uses_correct_template(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('order_manager:orders'))
        self.assertTemplateUsed(response, 'order_manager/pages/orders.html')

    def test_orders_manager_orders_url_uses_correct_context(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('order_manager:orders'))
        self.assertIn('orders', response.context)
