"""Factory boy factories
"""
import factory

from djflocash import models


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: "user-%d" % n)
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.username)


class OrderMixinFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.OrderMixin

    order_id = factory.Sequence(lambda n: "order-%d" % n)
    custom = factory.Sequence(lambda n: "custom-%d" % n)
    amount = 120.0
    item_name = factory.Sequence(lambda n: "item %d" % n)
    item_price = 120.0
    currency_code = "EUR"
    quantity = 1


class PayementFactory(OrderMixinFactory):
    client = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Payement


class NotificationFactory(OrderMixinFactory):
    sender_acct = factory.LazyAttribute(lambda obj: obj.payement.client.email)
    payement = factory.SubFactory(PayementFactory)
    trans_id = factory.Sequence(lambda n: "trans-%d" % n)
    fpn_id = factory.Sequence(lambda n: "fpn-%d" % n)
    status = 0
    status_msg = factory.LazyAttribute(
        lambda obj: models.Notification.KNOWN_STATUS.get(obj.status, ""))
    customer = factory.LazyAttribute(lambda obj: obj.payement.client.username)
    payer_email = factory.LazyAttribute(lambda obj: obj.payement.client.email)
    payment_channel = "Mobile"
    txn_partner_ref = factory.Sequence(lambda n: "txn-%d" % n)

    class Meta:
        model = models.Notification
