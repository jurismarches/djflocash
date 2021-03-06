import json

from django.urls import reverse
from django.test import TestCase

from djflocash.models import Notification
from djflocash.test import factories
from djflocash.test.mock import validate_notification_request_ok
from djflocash.test.mock import validate_notification_request_ko


class NotificationTestBase(TestCase):

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


@validate_notification_request_ok()
class NotificationReceiveTestCase(NotificationTestBase):

    def test_notification_url_uses_token(self, patched_validate):
        self.assertEqual(
            reverse("notification_receive"),
            "/notification/test-test-test/",
        )

    def test_valid_form(self, patched_validate):
        # corresponding payment
        payment = factories.PaymentFactory()
        # and another, to get it confused
        factories.PaymentFactory()
        form_data = dict(self.form_data)
        form_data["order_id"] = payment.order_id
        response = self.client.post(reverse("notification_receive"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "00")
        # validation was called
        self.assertTrue(patched_validate.called, True)
        # object created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.order_id, payment.order_id)
        self.assertEqual(notification.payment, payment)

    def test_valid_form_no_payment(self, patched_validate):
        response = self.client.post(reverse("notification_receive"), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "00")
        # object created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.order_id, "test order")
        # no associated payment
        self.assertIsNone(notification.payment)

    def test_error_form(self, patched_validate):
        response = self.client.post(reverse("notification_receive"), data={})
        self.assertEqual(response.status_code, 422)
        # incomplete
        data = dict(self.form_data)
        data.pop("order_id")
        response = self.client.post(reverse("notification_receive"), data=data)
        self.assertEqual(response.status_code, 422)
        errors = json.loads(response.content.decode("utf-8"))
        self.assertIn("order_id", errors)

    def test_get_fails(self, patched_validate):
        response = self.client.get(reverse("notification_receive"))
        self.assertEqual(response.status_code, 405)


@validate_notification_request_ko()
class NotificationReceiveInvalidTestCase(NotificationTestBase):

    def test_validation_request_fails(self, patched_validate):
        form_data = dict(self.form_data)
        response = self.client.post(reverse("notification_receive"), data=form_data)
        # validation was called
        self.assertTrue(patched_validate.called)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content.decode("utf-8"), "INVALID")
        # object not created
        self.assertEqual(Notification.objects.count(), 0)
