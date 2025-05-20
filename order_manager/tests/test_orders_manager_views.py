from django.test import TestCase
from django.urls import reverse, resolve
from order_manager import views
from .. models import Client, Order
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
import json


class OrdersViewsTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name='Cliente X')

        # Cria um superusuário
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )

        # Cria um usuário comum
        self.normal_user = User.objects.create_user(
            username='teste',
            password='senha123',
            first_name='joao'
        )

    def make_order(self, _status):
        _driver = self.admin_user
        order = Order.objects.create(
            delivery_date='2025-05-15', client=self.client_obj, driver=_driver, status=_status)

        return order

    def test_view_order_list_function_is_correct(self):
        view = resolve(reverse('order_manager:orders'))
        self.assertIs(view.func, views.order_list)

    def test_view_request_authentication(self):
        response = self.client.get(reverse('order_manager:orders'))
        self.assertRedirects(response, '/driver/login/?next=/orders/')

    def test_view_orders_load_template(self):
        self.client.force_login(self.admin_user)
        self.make_order('transito')
        response = self.client.get(reverse('order_manager:orders'))
        orders_reponse = response.context['orders']

        self.assertEqual(orders_reponse[0].client.name, 'Cliente X')
        self.assertEqual(
            orders_reponse[0].driver.username, 'admin')
        self.assertEqual(orders_reponse[0].status, 'transito')

    def test_view_order_register_has_data_in_session(self):
        self.client.force_login(self.admin_user)
        invalid_data = {'status': 25}
        self.client.post(
            reverse('order_manager:register_verify'), data=invalid_data)
        response = self.client.get(reverse('order_manager:register'))
        self.assertIn('form_data', response.wsgi_request.session)

    def test_view_order_register_dont_has_data_in_session(self):
        self.client.force_login(self.admin_user)
        self.client.post(reverse('order_manager:register_verify'))
        response = self.client.get(reverse('order_manager:register'))
        self.assertIn('form_data', response.wsgi_request.session)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_bound)  # form vazio

    def test_view_order_verify_receive_method_post(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('order_manager:register_verify'))
        self.assertEqual('POST', response.wsgi_request.method)
        self.assertIn('form_data', response.wsgi_request.session)

    def test_view_order_verify_rejects_get_method(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('order_manager:register_verify'))
        self.assertEqual(response.status_code, 404)

    def test_register_verify_valid_form_creates_order(self):
        self.client.force_login(self.admin_user)
        delivery_date = now().date() + timedelta(days=1)
        departure_time = now() + timedelta(days=1, hours=1)
        arrival_time = departure_time + timedelta(hours=2)
        delivery_completed = arrival_time + timedelta(hours=1)

        valid_data = {
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'departure_time': departure_time.strftime('%Y-%m-%dT%H:%M'),
            'arrival_time': arrival_time.strftime('%Y-%m-%dT%H:%M'),
            'delivery_completed': delivery_completed.strftime('%Y-%m-%dT%H:%M'),
            'driver': self.normal_user.pk,  # Precisa garantir que um driver exista
            'client': self.client_obj.pk,  # Precisa garantir que um client exista
            'status': 'concluida',  # Valor válido para status
        }
        response = self.client.post(
            reverse('order_manager:register_verify'), data=valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_manager:register'))
        # A ordem deve ter sido criada
        self.assertEqual(Order.objects.count(), 1)

        # A sessão não deve conter form_data
        session = self.client.session
        self.assertNotIn('form_data', session)

    def test_register_verify_valid_form_removes_form_data_from_session(self):
        self.client.force_login(self.admin_user)

        # Primeiro, manda um POST inválido para popular session['form_data']
        invalid_data = {'status': 25}  # status inválido
        self.client.post(reverse('order_manager:register_verify'),
                         data=invalid_data)

        session = self.client.session
        self.assertIn('form_data', session)  # Confirma que foi salvo

        # Agora, manda um POST válido
        from django.utils.timezone import now, timedelta
        delivery_date = now().date() + timedelta(days=1)
        departure_time = now() + timedelta(days=1, hours=1)
        arrival_time = departure_time + timedelta(hours=2)
        delivery_completed = arrival_time + timedelta(hours=1)

        valid_data = {
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'departure_time': departure_time.strftime('%Y-%m-%dT%H:%M'),
            'arrival_time': arrival_time.strftime('%Y-%m-%dT%H:%M'),
            'delivery_completed': delivery_completed.strftime('%Y-%m-%dT%H:%M'),
            'driver': self.normal_user.pk,  # Precisa garantir que um driver exista
            'client': self.client_obj.pk,  # Precisa garantir que um client exista
            'status': 'concluida',  # Valor válido para status
        }

        self.client.post(
            reverse('order_manager:register_verify'), data=valid_data)

        session = self.client.session
        # Essa linha cobre o if que apaga
        self.assertNotIn('form_data', session)

    def test_view_ordem_open_list_returns_only_pending_orders(self):
        self.client.force_login(self.admin_user)
        Order.objects.create(client=Client.objects.create(name='Cliente 1'),
                             delivery_date='2025-04-10', status='pendente')
        Order.objects.create(client=Client.objects.create(name='Cliente 2'),
                             delivery_date='2025-04-10', status='entregue')

        response = self.client.get(
            reverse('order_manager:open'))  # nome da URL
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['status'] == 'pendente'

    def test_view_orderm_open_list_json_fields(self):
        self.client.force_login(self.admin_user)
        Order.objects.create(
            client=self.client_obj,
            delivery_date='2025-04-10',
            status='pendente'
        )

        response = self.client.get(reverse('order_manager:open'))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)  # Garante que tem exatamente 1 item
        self.assertSetEqual(set(data[0].keys()), {
            'id', 'client__name', 'delivery_date', 'status'
        })
        self.assertEqual(data[0]['client__name'], 'Cliente X')

    def test_view_ordem_open_list_returns_empty_list_when_no_pending_orders(self):
        self.client.force_login(self.admin_user)
        Order.objects.create(client=self.client_obj,
                             delivery_date='2025-04-10',
                             status='entregue')

        response = self.client.get(reverse('order_manager:open'))
        assert response.status_code == 200
        assert response.json() == []

    def test_view_ordem_open_list_requires_login(self):
        response = self.client.get(reverse('order_manager:open'))
        # se redirecionar para login
        self.assertEqual(response.status_code, 302)

    def test_view_ordem_update_requires_login(self):
        response = self.client.get(reverse('order_manager:update'))
        # se redirecionar para login
        self.assertEqual(response.status_code, 302)

    def test_view_ordem_update_request_instead_post(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('order_manager:update'))
        self.assertNotEqual('POST', response.wsgi_request.method)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"message": "Método GET não permitido."}
        )

    def test_view_order_update_post_correct_json(self):
        self.client.force_login(self.admin_user)
        order = self.make_order('concluida')
        data = {'status': order.status,
                'id_order': order.pk, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertIn('message', data)
        self.assertEqual(data['message'],
                         'Status da entrega alterado')
        self.assertIn('order', data)
        order_data = data['order']
        self.assertEqual(order_data['id'], order.id)
        self.assertEqual(order_data['status'], 'concluida')
        self.assertEqual(order_data['driver'], self.normal_user.first_name)
        # # Confirma no banco se o status foi atualizado
        order.refresh_from_db()
        self.assertEqual(order.status, 'concluida')

    def test_view_order_update_post_wrong_json_status_key(self):
        self.client.force_login(self.admin_user)
        order = self.make_order('finalizada')
        # Campo status inexistente
        data = {'field': order.status,
                'id_order': order.pk, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Status do pedido não fornecido.')

        # Campo status correto e valor inexistente
        data = {'status': order.status,
                'id_order': order.pk, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Status fornecido inválido')

    def test_view_order_update_post_wrong_json_id_order_key(self):
        self.client.force_login(self.admin_user)
        order = self.make_order('pendente')
        # Campo id_order inexistente
        data = {'status': order.status,
                'order': order.pk, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'ID do pedido não fornecido.')

        # Campo id_order correto e valor inexistente
        data = {'status': order.status,
                'id_order': 56, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Orderm não encontrada.')

    def test_view_order_update_post_wrong_json_id_driver_key(self):
        self.client.force_login(self.admin_user)
        order = self.make_order('pendente')
        # Campo id_driver inexistente
        data = {'status': order.status,
                'id_order': order.pk, 'driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'ID do motorista não fornecido.')

        # Campo id_driver correto e valor inexistente
        data = {'status': order.status,
                'id_order': order.pk, 'id_driver': 88}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Motorista não cadastrado.')

    def test_view_order_update_has_open_session(self):
        self.client.force_login(self.admin_user)
        order = self.make_order('pendente')
        choice = {'id_order': order.pk, 'id_driver': self.normal_user.pk}
        self.client.post(reverse('order_manager:choice'), data=json.dumps(
            choice), content_type='application/json')

        # Sessão foi criada
        session = self.client.session
        self.assertIn('order_in_progress', session)

        data = {'status': order.status,
                'id_order': order.pk, 'id_driver': self.normal_user.pk}
        response = self.client.post(reverse('order_manager:update'), data=json.dumps(
            data), content_type='application/json')

        # Sessão excluida
        session = self.client.session
        self.assertNotIn('order_in_progress', session)

    def test_view_order_update_invalid_json_returns_400(self):
        self.client.force_login(self.admin_user)

        # Corpo JSON inválido (sem aspas nas chaves)
        invalid_json = '{status: pendente}'

        response = self.client.post(
            reverse('order_manager:update'),
            data=invalid_json,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Erro ao processar JSON.')
