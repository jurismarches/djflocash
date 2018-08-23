from django.test import TestCase
from django.contrib.auth.models import User

from djflocash.models import Payment


class PaymentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = User.objects.create(username="test")

    def test_payment_stays_after_user_cancellation(self):
        user = User.objects.create(username="transiant")
        payment = Payment.objects.create(
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
        # payment still exists
        payment = Payment.objects.get(pk=payment.pk)
        # but user is empty
        self.assertIsNone(payment.client_id)
