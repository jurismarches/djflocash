from django.test import TestCase

from djflocash.utils import get_ip_address


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
