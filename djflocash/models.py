from django.conf import settings
from django.db import models

from . import codes


class Payement(models.Model):
    """The payement model,
    It is intended to register a payement before user submit it,
    and then wait for notification from flocash about its acceptation or cancellation.

    we do not register fields that are not meaningful from our point of view (like merchant name).

    .. note:: the user is linked to django user, this is a default,
       you may subclass this model if you need, to point to your users.
    """

    order_id = models.CharField(max_length=25)
    custom = models.CharField(null=True, blank=True, max_length=25)
    amount = models.FloatField()
    item_name = models.CharField(max_length=250)
    item_price = models.FloatField()
    currency_code = models.CharField(
        choices=sorted(codes.CURRENCY_LABEL.items(), key=lambda c: c[1]),
        max_length=3,
    )
    quantity = models.IntegerField(default=1)
    country = models.CharField(
        null=True,
        choices=sorted(codes.COUNTRY_LABEL.items(), key=lambda c: c[1]),
        max_length=2,
    )
    payment_option = models.CharField(null=True, max_length=250)
    client = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.deletion.SET_NULL,  # we want to keep payments even if the user disapears
        null=True,
    )
