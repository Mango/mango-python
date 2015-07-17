PyMango
=======

This is a Python library that allows interaction with `Mango API <https://developers.getmango.com/en/api/?platform=python>`_.


Install
=======

You can get the library from ``PyPI`` using ``pip``::

    $ pip install pymango

If you want clone the repository, point it directly into our GitHub project::

    $ git clone https://github.com/Mango/mango-python.git


Documentation
=============

Documentation is available at https://developers.getmango.com/en/api/?platform=python

Usage
=====

Import the library and set your secret API key:

.. code-block:: python

    >>> import pymango as mango
    >>> mango.api_key = "your Mango secret API key"


Create a charge
---------------

In order to create a Charge, you must call the ``create()`` method with
the required arguments (see `API documentation <https://developers.getmango.com/en/api/charges/?platform=python#arguments>`_):

.. code-block:: python

    >>> charge = mango.Charges.create(amount=2000, email="test@example.org", token="token_mwhushs06o62aruq9n3pmvu7f0ia696y")
    >>> print charge.get("uid")
    charge_72t1r7vmb9pknrl4otg6xy3wrkwrrpzt
    >>> print charge.get("paid")
    True


Get single Charge
-----------------

When you have a Charge ``uid``, you can get a full detail using the ``get()`` method:

.. code-block:: python

    >>> mango.Charges.get("charge_72t1r7vmb9pknrl4otg6xy3wrkwrrpzt")
    {
        u'customer': u'',
        u'deposit_eta': u'2013-04-09',
        u'queue_uid': u'',
        u'fee': 12,
        u'annual_interest_pct': u'',
        u'refunded': False,
        u'created_at': u'2013-09-04 20:23:28',
        u'live': False,
        u'amount_gross': 1212,
        u'paid': False,
        u'failure_message': u'',
        u'origin': u'api',
        u'amount': 1212,
        u'installments': 1,
        u'plastic': {
            u'last4': u'4242',
            u'exp_year': 2015,
            u'exp_month': 11,
            u'type': u'visa',
            u'holdername': u'Test Test'
        },
        u'uid': u'charge_72t1r7vmb9pknrl4otg6xy3wrkwrrpzt',
        u'email': u'test@getmango.com',
        u'card': u'',
        u'description': u''
    }

You can also work with all the other resources authenticated with a secret API Key:

* `Charges <https://developers.getmango.com/en/api/charges/?platform=python>`_
* `Refunds <https://developers.getmango.com/en/api/refunds/?platform=python>`_
* `Customers <https://developers.getmango.com/en/api/customers/?platform=python>`_
* `Cards <https://developers.getmango.com/en/api/cards/?platform=python>`_
* `Queue <https://developers.getmango.com/en/api/queue/?platform=python>`_
* `Installments <https://developers.getmango.com/en/api/installments/?platform=python>`_
* `Promotions <https://developers.getmango.com/en/api/promotions/?platform=python>`_
* `Coupons <https://developers.getmango.com/en/api/coupons/?platform=python>`_


Tests
=====

Install testing dependencies::

    $ pip install nose

To run the tests you'll need Mango API keys (mode Sandbox)::

    $ export MANGO_SECRET_TEST_KEY=secret_test_qawsedrftgyhujikolp
    $ export MANGO_PUBLIC_TEST_KEY=public_test_aqswdefrgthyjukilon


Run the tests
-------------

Use ``nosetests`` to run the complete tests suite::

    $ nosetests pymango/tests/


License
=======

`MIT <http://opensource.org/licenses/MIT>`_, see LICENSE file.
