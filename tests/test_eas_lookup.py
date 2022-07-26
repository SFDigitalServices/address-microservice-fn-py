""" Test for eas/json endpoint """
import json
from unittest.mock import patch
import azure.functions as func
from eas_lookup import main

def test_eas_lookup_function():
    """ test_eas_lookup_function """

    search = "49 south"
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/eas/lookup',
        params={'search': search})

    # Call the function.
    resp = main(req)

    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'success'
    assert len(resp_json['data']['items']) > 0
    assert search.upper() in resp_json['data']['items'][0]['address']

def test_eas_lookup_function_error():
    """ test_eas_lookup_function_error """
    # Construct a mock HTTP request.
    with patch.dict("os.environ", {"EAS_API_URL": "", "ADDRESS_SVC_APP_TOKEN": ""}):
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/eas/lookup')

        # Call the function.
        resp = main(req)

        # Check the output.
        assert resp.status_code == 500
