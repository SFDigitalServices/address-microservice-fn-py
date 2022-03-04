""" Test for abe/json endpoint """
import json
from unittest.mock import patch
import azure.functions as func
from abe_json import main

def test_abe_json_function():
    """ test_abe_json_function """

    requests_params = [
        {},
        {"format": "eas", "$select": "address"},
        {"format": "eas", "$select": "address", "$where": "parcel_number IS NOT NULL"}]
    for params in requests_params:

        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/abe/json',
            params=params)

        # Call the function.
        resp = main(req)
        # print response body
        print(resp.get_body())
        # loads response body as json
        resp_json = json.loads(resp.get_body())

        # Check the output.
        assert resp_json['status'] == 'success'
        assert len(resp_json['data']['items']) > 0

def test_abe_json_function_request_error():
    """ test_abe_json_function_func_error """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/abe/json',
        params={'hello': 'world'})

    # Call the function.
    resp = main(req)

    resp_json = json.loads(resp.get_body())
    print(resp_json)
    # Check the output.
    assert resp_json['error']

def test_abe_json_function_url_error():
    """ test_abe_json_function_url_error """
    # Construct a mock HTTP request.
    with patch.dict("os.environ", {"ABE_API_URL": "", "ADDRESS_SVC_APP_TOKEN": ""}):
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/abe/json')

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())
        # Check the output.
        assert resp_json['status'] == 'error'
