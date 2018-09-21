from unittest import mock

from django.http import HttpRequest
from django.test import TestCase

from djflocash.utils import get_ip_address, validate_notification_request


class FakeRequest:

    def __init__(self):
        self.META = {}


class UtilsTestCase(TestCase):

    def test_get_ip_address_forwarded(self):
        request = FakeRequest()
        request.META["REMOTE_ADDR"] = "20.20.0.20"
        request.META["HTTP_X_FORWARDED_FOR"] = "12.34.56.98, 23.45.67.99"
        request.META["HTTP_FORWARDED"] = (
            "for=12.34.56.78;host=example.com;proto=https, for=23.45.67.89")
        self.assertEqual(get_ip_address(request), "12.34.56.78")

    def test_get_ip_address_x_forwarded_for(self):
        request = FakeRequest()
        request.META["REMOTE_ADDR"] = "20.20.0.20"
        request.META["HTTP_X_FORWARDED_FOR"] = "12.34.56.98, 23.45.67.99"
        self.assertEqual(get_ip_address(request), "12.34.56.98")

    def test_get_ip_address_remote_addr(self):
        request = FakeRequest()
        request.META["REMOTE_ADDR"] = "20.20.0.20"
        self.assertEqual(get_ip_address(request), "20.20.0.20")

    @mock.patch("requests.post")
    def test_validate_notification_request(self, patched_post):
        req = HttpRequest()
        req.POST["trans_id"] = "test_trans_id"
        req.POST["custom"] = "test_custom"
        validate_notification_request(req.POST)
        expected_url = "https://flocash.example.com/validateNotify.do"
        expected_params = {
            "trans_id": ["test_trans_id"],
            "custom": ["test_custom"],
            "cmd": "notify-validate",
        }
        patched_post.assert_called_with(expected_url, expected_params)
