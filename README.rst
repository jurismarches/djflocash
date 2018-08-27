DJFlocash
###########

|pypi-version| |travis|

Python helpers to use https://www.flocash.com/ Payement API in Django.

This product is not complete, but contributions are welcome.

Flocash is a gateway payement API
enabling payement in a lot of african countries
through credit cards, mobile phone payements and more.

This library gives you some re-usable components to use in Django.

.. important:: This program IS NOT an official library of flocash.
     flocash is a registered trademark of Flocash ltd.


Setting up
==========

In your project, you can either create your own models that inherit the base one,
or use the proposed one directly.

In the first case, you may want to connect your model to handlers defined in `signals.py`.

For both cases, add djflocash to your `INSTALLED_APPS` setting.

You have to define some mandatory settings:

* FLOCASH_BASE_URL the base url of flocash service
* FLOCASH_PAYMENT_URI the uri handling ecommerce payment (will be urljoined to base url)
* FLOCASH_MERCHANT, FLOCASH_MERCHANT_NAME your merchant account and display name

and some optionnal one:

* FLOCASH_PAYMENT_MODEL is the payment model in case you don't use provided model.

Usage
=====


The idea is that your visitor will submit a payment through his browser. For this you need to build the form, you can do this using `forms.OrderForm`, if you submit it through javascript you may use the `to_dict` method.

You can expose the `views.NotificationReceive` view (or your own based on it) to get notifications (successful or canceled) payment. It creates a `models.Notification` instance and associate it to the `models.Payment` having same `order_id` if it exists.

A possible workflow is thus the following:

- you create a `models.Payment` corresponding to your visitor basket
- you use `forms.OrderForm.from_payment` to generate corresponding form and render it in visitor browser (using hidden fields)
- visitor submit the form to flocash and is redirected to flocash payment portal where he completes the transaction
- flocash submit the payment notification through `views.NotificationReceive`, and some custom handler you attached on eg. `post_save` signal make the order effective in you system
- visitors gets back to your site where you tell him his purchase is effective

.. |pypi-version| image:: https://img.shields.io/pypi/v/djflocash.svg
    :target: https://pypi.python.org/pypi/djflocash
    :alt: Latest PyPI version

.. |travis| image:: http://img.shields.io/travis/jurismarches/djflocash/master.svg?style=flat
    :target: https://travis-ci.org/jurismarches/djflocash
    :alt: Travis status

.. |license| image:: https://img.shields.io/github/license/jurismarches/djflocash.svg   
    :target: https://github.com/jurismarches/djflocash/blob/master/LICENSE
    :alt: LGPL license
