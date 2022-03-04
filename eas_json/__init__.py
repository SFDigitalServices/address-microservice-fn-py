""" eas/json init file """
import os
import json
import logging
import requests
import jsend
import azure.functions as func
from shared_code.common import func_json_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for eas/json """
    logging.info('EAS JSON processed a request.')

    try:
        response = requests.get(
            os.getenv('EAS_API_URL'),
            params=req.params,
            headers={'X-App-Token': os.getenv('ADDRESS_SVC_APP_TOKEN')}
        )

        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        return func_json_response(response, headers)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("EAS JSON error occurred: %s", err)
        msg_error = "This endpoint encountered an error. {}".format(err)
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
