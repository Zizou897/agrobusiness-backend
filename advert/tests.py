from django.test import Client, TestCase
from django.urls import reverse


# Create your tests here.
class ProductOrderUpdateStatusViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username="seller001", password="Password2023@@")

    def test_order_quantity_is_greater_than_product_quantity_error(self):
        response = self.client.post(
            reverse(
                "update-order-status",
                kwargs={"order_id": "060ef98d-ab91-424d-8df5-ce38cc20a466"},
            ),
            {
                "status": "DELIVERED",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.url, "/advert/product_orders/")
