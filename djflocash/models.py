from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import codes


AMOUNT_MAX_DIGITS = getattr(settings, "FLOCASH_AMOUNT_MAX_DIGITS", 10)
AMOUNT_DECIMAL_PLACES = getattr(settings, "FLOCASH_AMOUNT_DECIMAL_PLACES", 2)


class OrderMixin(models.Model):
    """fields making up an order
    """
    order_id = models.CharField(
        verbose_name=_("Unique transaction ID of the order"),
        max_length=25,
    )
    custom = models.CharField(
        verbose_name=_("Merchant defined field"),
        null=True, blank=True, max_length=25,
    )
    amount = models.DecimalField(
        max_digits=AMOUNT_MAX_DIGITS, decimal_places=AMOUNT_DECIMAL_PLACES)
    item_name = models.CharField(max_length=250)
    item_price = models.DecimalField(
        max_digits=AMOUNT_MAX_DIGITS, decimal_places=AMOUNT_DECIMAL_PLACES)
    currency_code = models.CharField(
        choices=sorted(codes.CURRENCY_LABEL.items(), key=lambda c: c[1]),
        max_length=3,
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        abstract = True


class Payment(OrderMixin):
    """The payment model,
    It is intended to register a payment before user submit it,
    and then wait for notification from flocash about its acceptation or cancellation.

    we do not register fields that are not meaningful from our point of view (like merchant name).

    .. note:: the user is linked to django user, this is a default,
       you may subclass this model if you need, to point to your users.
    """
    country = models.CharField(
        null=True,
        choices=sorted(codes.COUNTRY_LABEL.items(), key=lambda c: c[1]),
        max_length=2,
    )
    payment_option = models.CharField(
        verbose_name=_("Pre-set payment option for selected country"),
        null=True,
        max_length=250
    )
    client = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.deletion.SET_NULL,  # we want to keep payments even if the user disapears
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)


class Notification(OrderMixin):
    """A notification received from Flocash
    """

    # we list here known status, but do not enforce them into field to be tolerant
    KNOWN_STATUS = {
        0: "Payment is successful.",
        1: "Payment was aborted.",
        2: "Customer cancelled the payment.",
        3: "Transaction was not authorized.",
        4: "Payment is pending.",
    }

    #: status known to mean payment is ok
    PAID_STATUS = {0}

    sender_acct = models.CharField(
        verbose_name=_("Sender Account"),
        max_length=50,
    )
    trans_id = models.CharField(
        verbose_name=_("Unique transaction ID. If error, the value is 0"),
        max_length=20,
    )
    fpn_id = models.CharField(
        verbose_name=_("Unique FloCash ID"),
        max_length=20,
    )
    status = models.PositiveSmallIntegerField()
    status_msg = models.CharField(
        verbose_name=_("Status message"),
        max_length=250,
    )
    customer = models.CharField(
        verbose_name=_("Customer Name"),
        blank=True,
        max_length=250,
    )
    payer_email = models.CharField(
        verbose_name=_("Customer's email"),
        blank=True,
        max_length=250,
    )
    payment_channel = models.CharField(max_length=250)
    txn_partner_ref = models.CharField(
        verbose_name=_("Transaction reference return from bank"),
        max_length=250,
    )
    created = models.DateTimeField(auto_now_add=True)

    payment = models.ForeignKey(
        to=getattr(settings, "FLOCASH_PAYMENT_MODEL", Payment),
        related_name='notifications',
        on_delete=models.deletion.SET_NULL,
        null=True)

    @property
    def _payment_type(self):
        return self._meta.get_field("payment").remote_field.model

    def find_payment(self):
        """try to find payment associated with notification
        """
        try:
            return self._payment_type.objects.get(order_id=self.order_id)
        except (Payment.DoesNotExist, Payment.MultipleObjectsReturned):
            return None

    @property
    def successful(self):
        return self.status in self.PAID_STATUS
