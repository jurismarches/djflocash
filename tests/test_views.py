import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from djflocash.models import Notification
from djflocash.test import factories


class NotificationReceiveTestCase(TestCase):

    def setUp(self):
        self.form_data = dict(
            merchant="test@merchant.com",
            custom="test custom",
            order_id="test order",
            amount=123,
            item_name="test item",
            item_price=123,
            currency_code="EUR",
            quantity=1,
            sender_acct="test sender",
            trans_id="test trans",
            fpn_id="test fpn",
            status=0,
            status_msg="test status",
            customer="test@customer.com",
            payer_email="payer@customer.com",
            payment_channel="test chan",
            txn_partner_ref="test partner ref",
        )

    def test_valid_form(self):
        # corresponding payement
        payement = factories.PayementFactory()
        # and another, to get it confused
        factories.PayementFactory()
        form_data = dict(self.form_data)
        form_data["order_id"] = payement.order_id
        response = self.client.post(reverse("notification_receive"), data=form_data)
        self.assertEqual(response.status_code, 200)
        # object created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.order_id, payement.order_id)
        self.assertEqual(notification.payement, payement)

    def test_valid_form_no_payement(self):
        response = self.client.post(reverse("notification_receive"), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        # object created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.order_id, "test order")
        # no associated payement
        self.assertIsNone(notification.payement)

    def test_error_form(self):
        response = self.client.post(reverse("notification_receive"), data={})
        self.assertEqual(response.status_code, 422)
        # incomplete
        data = dict(self.form_data)
        data.pop("order_id")
        response = self.client.post(reverse("notification_receive"), data=data)
        self.assertEqual(response.status_code, 422)
        errors = json.loads(response.content.decode("utf-8"))
        self.assertIn("order_id", errors)

    def test_get_fails(self):
        response = self.client.get(reverse("notification_receive"))
        self.assertEqual(response.status_code, 405)
