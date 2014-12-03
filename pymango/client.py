"""
Mango Python Library Client
"""
import json

import requests
from requests.exceptions import ConnectionError

from .error import UnableToConnect, AuthenticationError, NotFound, \
    InputValidationError, InputValidationGenericError, \
    UnhandledError, MethodNotAllowed


BASE_URL = "https://api.getmango.com"
HEADERS = {"content-type": "application/json"}


def req(api_key, method, endpoint, data=None, params=None):
    """
    Make request and return a Python object from the JSON response. If
    HTTP method is DELETE return True for 204 response, false otherwise.

    :param api_key: String with the API key
    :param method: String with the HTTP method
    :param endpoint: String with the URL
    :param data: Dictionary with data that will be sent
    :param params: Dictionary with query strings
    :return: Native python object resulting of the JSON deserialization of the API response
    """
    if data:
        data = json.dumps(data)

    try:
        response = requests.request(
            method,
            build_url(endpoint),
            data=data,
            params=params,
            auth=(api_key, ""),
            headers=HEADERS
        )
    except ConnectionError:
        raise UnableToConnect

    # Success
    if 200 <= response.status_code <= 206:
        if response.request.method == "DELETE":
            return response.status_code == 204 or response.status_code == 200

        return response.json()

    # Error handling
    if response.status_code == 400:
        try:
            input_validation_error = response.json()
            errors = input_validation_error.get("errors")[0]
            error_code, error_message = errors.items()[0]
        except:
            raise InputValidationGenericError("{status_code}: {text}".format(
                status_code=response.status_code,
                text=response.text
            ))
        raise InputValidationError(error_code, error_message)
    elif response.status_code == 401:
        raise AuthenticationError
    elif response.status_code == 404:
        raise NotFound
    elif response.status_code == 405:
        raise MethodNotAllowed

    raise UnhandledError("{status_code}: {text}".format(
        status_code=response.status_code,
        text=response.text
    ))


def build_url(endpoint):
    """
    Build complete URL from API endpoint

    :param endpoint: String with the endpoint, ex: /v1/charges/
    :return: String with complete URL, ex: https://api.getmango.com/v1/charges/
    """
    return "{base_url}/{endpoint}".format(
        base_url=BASE_URL,
        endpoint=endpoint
    )
