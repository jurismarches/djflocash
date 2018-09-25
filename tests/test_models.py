from django.test import TestCase
from django.contrib.auth.models import User

from djflocash.models import Payment
from djflocash.test.factories import PaymentFactory, NotificationFactory


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

    def test_is_pending_new_object(self):
        p = PaymentFactory.build()
        self.assertFalse(p.is_pending)

    def test_pending_status_filtering(self):
        pending = PaymentFactory()
        NotificationFactory(payment=pending, status=4)
        no_notification = PaymentFactory()
        cancelled = PaymentFactory()
        NotificationFactory(payment=cancelled, status=2)
        unauthorized = PaymentFactory()
        NotificationFactory(payment=cancelled, status=3)

        self.assertEqual(
            list(Payment.objects.pending().values_list("id", flat=True)),
            [pending.pk],
        )
        self.assertTrue(pending.is_pending)
        self.assertFalse(no_notification.is_pending)
        self.assertFalse(cancelled.is_pending)
        self.assertFalse(unauthorized.is_pending)
