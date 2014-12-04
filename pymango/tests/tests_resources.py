"""
PyMango Tests for Resources
"""
import os
from random import randint

from nose.tools import eq_, ok_, raises

import pymango as mango

# Setup
mango.api_key = os.getenv("MANGO_SECRET_TEST_KEY")
public_test_key = os.getenv("MANGO_PUBLIC_TEST_KEY")

TEST_CARD = {
    "number": "4507990000000010",
    "exp_month": "12",
    "exp_year": "2020",
    "holdername": "John Doe",
    "type": "visa",
    "ccv": "123"
}


#
# Utils
#
def _create_token():
    token_response = mango.client.req(
        public_test_key,
        "post",
        "v1/tokens/",
        data=TEST_CARD
    )
    return token_response.get("uid")


def _create_ccv():
    ccv_response = mango.client.req(
        public_test_key,
        "post",
        "v1/ccvs/",
        data={"ccv": randint(100, 999)}
    )
    return ccv_response.get("uid")


#
# Charges
#
def test_charges_create():
    """Should create a charge using a token"""
    amount = 1000
    email = "test-pymango@example.org"
    charge = mango.Charges.create(amount=amount, email=email, token=_create_token())
    ok_(charge)
    ok_(charge.get("uid"))
    eq_(amount, charge.get("amount"))
    eq_(email, charge.get("email"))
    ok_(charge.get("paid"))


def test_charges_list():
    """Should return a list of charges"""
    eq_(list, type(mango.Charges.list()))


def test_charges_get():
    """Should get a charge"""
    charge_uid = mango.Charges.list()[0].get("uid")
    charge = mango.Charges.get(charge_uid)
    ok_(charge)
    ok_(charge.get("uid"))


#
# Refunds
#
def test_refunds_create():
    """Should refund a charge"""
    amount = 1000
    email = "test-pymango@example.org"
    charge = mango.Charges.create(amount=amount, email=email, token=_create_token())
    ok_(charge)
    charge_uid = charge.get("uid")
    ok_(charge_uid)
    refund = mango.Refunds.create(charge=charge_uid)
    ok_(refund)
    eq_(refund.get("charge"), charge_uid)


def test_refunds_list():
    """Should return a list of customers"""
    eq_(list, type(mango.Refunds.list()))


def test_refunds_get():
    """Should get a refund"""
    refund_uid = mango.Refunds.list()[0].get("uid")
    refund = mango.Refunds.get(refund_uid)
    ok_(refund)
    ok_(refund.get("uid"))
    ok_(refund.get("charge"))


#
# Customers
#
def test_customers_create():
    """Should create a customer"""
    customer_data = {"email": "test-pymango@example.org", "name": "Test Customer"}
    customer = mango.Customers.create(**customer_data)
    ok_(customer)
    for k, v in customer_data.iteritems():
        eq_(v, customer.get(k))


def test_customers_list():
    """Should return a list of customers"""
    eq_(list, type(mango.Customers.list()))


def test_customers_get():
    """Should get a customer"""
    customer_uid = mango.Customers.list()[0].get("uid")
    customer = mango.Customers.get(customer_uid)
    ok_(customer)
    ok_(customer.get("uid"))


def test_customers_update():
    """Should update customer data"""
    sample_name = "test-pymango-{0}".format(randint(1000, 999999))
    customer_uid = mango.Customers.list()[0].get("uid")
    ok_(mango.Customers.update(customer_uid, name=sample_name))
    eq_(sample_name, mango.Customers.get(customer_uid).get("name"))


@raises(mango.error.NotFound)
def test_customers_delete():
    """Should delete a customer"""
    customer_uid = mango.Customers.list()[0].get("uid")
    ok_(mango.Customers.delete(customer_uid))
    mango.Customers.get(customer_uid)


#
# Cards
#
def test_cards_create():
    """Should create a card"""
    card = mango.Cards.create(customer=mango.Customers.list()[0].get("uid"), token=_create_token())
    ok_(card)
    ok_(card.get("uid"))


def test_cards_list():
    """Should return a list of cards"""
    eq_(list, type(mango.Cards.list()))


def test_cards_get():
    """Should get a card"""
    card = mango.Cards.get(mango.Cards.list()[0].get("uid"))
    ok_(card)


def test_cards_update():
    """Should update card CCV"""
    card_uid = mango.Cards.get(mango.Cards.list()[0].get("uid")).get("uid")
    ok_(mango.Cards.update(card_uid, ccv=_create_ccv()))


@raises(mango.error.NotFound)
def test_cards_delete():
    """Should delete a Card"""
    card_uid = mango.Cards.get(mango.Cards.list()[0].get("uid"))
    ok_(mango.Cards.delete(card_uid))
    mango.Cards.get(card_uid)


#
# Queue
#
def test_queue_list():
    """Should return a list of queued resources"""
    eq_(list, type(mango.Queue.list()))


def test_queue_get():
    """Should get a queue element"""
    charge = mango.Charges.create(amount=1000, email="test-pymango@example.org", token=_create_token(), enqueue=True)
    queue_uid = charge.get("queue")
    queued_charge = mango.Queue.get(queue_uid)
    ok_(queued_charge)
    eq_(queued_charge.get("resource_uid"), charge.get("uid"))


@raises(mango.error.NotFound)
def test_queue_delete():
    """Should delete an element from the queue"""
    charge = mango.Charges.create(amount=1000, email="test-pymango@example.org", token=_create_token(), enqueue=True)
    queue_uid = charge.get("queue")
    ok_(mango.Queue.delete(queue_uid))
    mango.Queue.get(queue_uid)


def test_queue_delete_all():
    """Should delete all elements from que queue"""
    charge = mango.Charges.create(amount=1000, email="test-pymango@example.org", token=_create_token(), enqueue=True)
    ok_(charge)
    ok_(charge.get("queue"))
    ok_(mango.Queue.delete_all())
    eq_(0, len(mango.Queue.list()))


#
# Installments
#
def test_installments_list():
    """Should return a list of queued resources"""
    eq_(list, type(mango.Queue.list()))


def test_installments_list_filters():
    """Should return a filtered list of installment resources"""
    installments = mango.Installments.list(cardtype="visa", amount="5000")
    for installment in installments:
        eq_("visa", installment.get("cardtype"))
        eq_(5000, installment.get("amount"))
