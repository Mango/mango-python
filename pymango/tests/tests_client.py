"""
PyMango Tests for Client
"""
import os

from nose.tools import eq_
from pymango import client

# Get API key from environment
TEST_API_KEY = os.getenv('MANGO_SECRET_TEST_KEY')


def test_client_build_url():
    """Should build a complete URL for an endpoint consisting on version + resource"""
    eq_("{0}/{1}".format(client.BASE_URL, "v1/charges/"), client.build_url("v1/charges/"))


def test_client_get():
    """Should make a GET request and return a list"""
    response = client.req(TEST_API_KEY, "get", "v1/charges/")
    eq_(list, type(response))


def test_client_post():
    """Should make a request and send JSON data with correct content type"""
    test_data = {"email": "test-pymango@example.org", "name": "Test Customer"}
    response = client.req(TEST_API_KEY, "post", "v1/customers/", data=test_data)
    for k in test_data.keys():
        eq_(test_data.get(k), response.get(k))


def test_client_querystring():
    """Should make a request and send parameters"""
    test_params = {"cardtype": "visa"}
    response = client.req(TEST_API_KEY, "get", "v1/installments/", params=test_params)
    eq_(list, type(response))
    for interest in response:
        eq_("visa", interest.get("cardtype"))