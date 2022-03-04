""" eas/lookup init file """
import os
import json
import logging
import requests
import azure.functions as func
from shared_code.common import func_json_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for eas/lookup """

    logging.info('EAS Lookup processed a request.')

    try:
        params  = req.params.copy()
        if params['search'] :
            params['$where'] = \
                "address like upper('{}%') AND parcel_number IS NOT NULL"\
                .format(params['search'])
            del params['search']

        response = requests.get(
            os.getenv('EAS_API_URL'),
            params=params,
            headers={'X-App-Token': os.getenv('ADDRESS_SVC_APP_TOKEN')}
        )

        headers = {
            "Cache-Control": "s-maxage=1, stale-while-revalidate, max-age={}"\
                .format(os.getenv('ADDRESS_SVC_CACHE_MAX_AGE')),
            "Access-Control-Allow-Origin": "*"
        }

        return func_json_response(response, headers)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("EAS Lookup error occurred: %s", err)
        return func.HttpResponse(f"This endpoint encountered an error. {err}", status_code=500)
