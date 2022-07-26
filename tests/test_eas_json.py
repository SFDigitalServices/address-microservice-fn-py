""" Test for eas/json endpoint """
import json
from unittest.mock import patch
import azure.functions as func
from eas_json import main

def test_eas_json_function():
    """ test_eas_json_function """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/eas/json')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'success'
    assert len(resp_json['data']['items']) > 0

def test_eas_json_function_request_error():
    """ test_eas_json_function_func_error """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/eas/json',
        params={'hello': 'world'})

    # Call the function.
    resp = main(req)

    resp_json = json.loads(resp.get_body())
    print(resp_json)
    # Check the output.
    assert resp_json['error']

def test_eas_json_function_url_error():
    """ test_eas_json_function_url_error """
    # Construct a mock HTTP request.
    with patch.dict("os.environ", {"EAS_API_URL": "", "ADDRESS_SVC_APP_TOKEN": ""}):
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/eas/json')

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())
        # Check the output.
        assert resp_json['status'] == 'error'
