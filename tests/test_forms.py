import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test.utils import override_settings

from djflocash.forms import OrderForm
from djflocash.models import Payement


@override_settings(FLOCASH_MERCHANT="test@merchant.com")
class OrderFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = User.objects.create(username="test")
        cls.payement = Payement.objects.create(
            order_id="test order",
            custom="test custom",
            client=cls.client,
            amount=400,
            item_name="test item",
            item_price=400,
            currency_code="EUR",
            quantity=1,
        )

    def test_create_from_payement(self):
        payement = self.payement
        result = OrderForm.from_payement(payement)
        self.assertTrue(result.is_valid())
        data = result.cleaned_data
        self.assertEqual(data["order_id"], payement.order_id)
        self.assertEqual(data["custom"], payement.custom)
        self.assertEqual(data["amount"], payement.amount)
        self.assertEqual(data["quantity"], payement.quantity)
        self.assertEqual(data["merchant"], "test@merchant.com")
        self.assertEqual(data["user_firstname"], "")

    @override_settings(FLOCASH_MERCHANT_NAME="test merchant name")
    def test_create_from_payement_with_settings(self):
        result = OrderForm.from_payement(self.payement)
        self.assertTrue(result.is_valid())
        data = result.cleaned_data
        self.assertEqual(data["merchant_name"], "test merchant name")

    def test_create_from_payement_overrides(self):
        result = OrderForm.from_payement(self.payement, amount=800, custom="new custom")
        self.assertTrue(result.is_valid())
        data = result.cleaned_data
        self.assertEqual(data["amount"], 800)
        self.assertEqual(data["custom"], "new custom")

    def test_to_dict_raise_if_invalid(self):
        order = OrderForm.from_payement(self.payement)
        order.is_valid()
        data = order.cleaned_data
        # remove merchant
        del data["merchant"]
        broken_order = OrderForm(data)
        with self.assertRaises(ValidationError):
            broken_order.to_dict()

    def test_to_dict(self):
        result = OrderForm.from_payement(self.payement).to_dict()
        self.assertEqual(result["amount"], 400)
        self.assertEqual(result["custom"], "test custom")
        self.assertEqual(result["quantity"], 1)
        self.assertEqual(result["merchant_name"], "test name")
        self.assertNotIn("user_firstname", result)
        self.assertNotIn("image_url", result)
        # assert we only have jsonable data
        json.dumps(result)
