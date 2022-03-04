""" Test for abe/json endpoint """
import json
from unittest.mock import patch
import azure.functions as func
from abe_lookup import main

def test_abe_lookup_function():
    """ test_abe_lookup_function """

    search = "1 south"
    requests_params = [{'search': search}, {'search': search, '$select': 'address'}]
    for params in requests_params:
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/abe/lookup',
            params=params)

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())

        # Check the output.
        assert resp_json['status'] == 'success'
        assert len(resp_json['data']['items']) > 0
        assert search.upper() in resp_json['data']['items'][0]['address']

def test_abe_lookup_function_error():
    """ test_abe_lookup_function_error """
    # Construct a mock HTTP request.
    with patch.dict("os.environ", {"ABE_API_URL": "", "ADDRESS_SVC_APP_TOKEN": ""}):
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/abe/lookup')

        # Call the function.
        resp = main(req)

        # Check the output.
        assert resp.status_code == 500
