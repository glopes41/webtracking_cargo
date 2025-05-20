from .test_orders_manager_views import OrdersViewsTest
from django.core.exceptions import ValidationError


class OrdersModelsTest(OrdersViewsTest):
    def setUp(self):
        # self.resp = self.make_client()
        return super().setUp()

    # def test_test_models(self):
    #     self.resp.name = 'A' * 65
    #     with self.assertRaises(ValidationError):
    #         self.resp.full_clean()
