""" abe/lookup init file """
import os
import json
import logging
import requests
import azure.functions as func
from shared_code.common import func_json_response, abe_to_eas_fields_query

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for abe/lookup """

    logging.info('ABE Lookup processed a request.')

    try:
        params  = req.params.copy()

        if 'search' in params :
            params['$where'] = \
                "address like upper('{}%') AND block IS NOT NULL and lot IS NOT NULL"\
                .format(params['search'])
            if '$select' in params:
                params['$select'] = abe_to_eas_fields_query(params['$select'])
            else:
                params['$select'] = abe_to_eas_fields_query("address")
            del params['search']

        response = requests.get(
            os.getenv('ABE_API_URL'),
            headers={
                'Authorization': 'Basic ' + os.getenv('ADDRESS_SVC_AUTH_API_KEY'),
                'X-App-Token': os.getenv('ADDRESS_SVC_APP_TOKEN')
            },
            params=params
        )

        headers = {
            "Cache-Control": "s-maxage=1, stale-while-revalidate, max-age={}"\
                .format(os.getenv('ADDRESS_SVC_CACHE_MAX_AGE')),
            "Access-Control-Allow-Origin": "*"
        }

        return func_json_response(response, headers)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("ABE Lookup error occurred: %s", err)
        return func.HttpResponse(f"This endpoint encountered an error. {err}", status_code=500)
