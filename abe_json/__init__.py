""" abe/json init file """
import os
import json
import logging
import requests
import jsend
import azure.functions as func
from shared_code.common import func_json_response,abe_to_eas_fields_query

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for abe/json """
    logging.info('ABE JSON processed a request.')

    try:
        params  = req.params.copy()
        if "format" in params:
            if params['format'] == "eas":
                if "$where" in params and "parcel_number" in params['$where'] \
                    and ("$select" not in params or "parcel_number" not in params['$select']):
                    params['$select'] += ",parcel_number"
                if "$select" in params:
                    params['$select'] = abe_to_eas_fields_query(params['$select'])
            del params['format']
        response = requests.get(
            os.getenv('ABE_API_URL'),
            params=params,
            headers={
                'Authorization': 'Basic ' + os.getenv('ADDRESS_SVC_AUTH_API_KEY'),
                'X-App-Token': os.getenv('ADDRESS_SVC_APP_TOKEN')
            }
        )
        print(params)
        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        return func_json_response(response, headers)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("ABE JSON error occurred: %s", err)
        msg_error = "This endpoint encountered an error. {}".format(err)
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
