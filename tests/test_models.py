from django.test import TestCase
from django.contrib.auth.models import User

from djflocash.models import Payement


class PayementTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = User.objects.create(username="test")

    def test_payement_stays_after_user_cancellation(self):
        user = User.objects.create(username="transiant")
        payement = Payement.objects.create(
            order_id="test order",
            custom="test custom",
            client=user,
            amount=400,
            item_name="test item",
            item_price=400,
            currency_code="EUR",
            quantity=1,
        )
        user.delete()
        # payement still exists
        payement = Payement.objects.get(pk=payement.pk)
        # but user is empty
        self.assertIsNone(payement.client_id)
