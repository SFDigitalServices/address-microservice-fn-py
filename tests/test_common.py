# pylint: disable=consider-using-with
""" Test Common functions """
import json
from unittest import mock

from shared_code import common


def test_func_json_response_error():
    """test func_json_response()"""

    response500 = mock.Mock()
    response500.status_code = 500
    response500.text = json.dumps("500 Internal Server Error")
    jsend_response = common.func_json_response(response500)
    jsend_json = json.loads(jsend_response.get_body())
    assert jsend_response.status_code == 500
    assert jsend_json["status"] == "error"
