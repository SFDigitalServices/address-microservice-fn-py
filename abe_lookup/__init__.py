""" abe/lookup init file """
import os
import logging
import azure.functions as func
from shared_code.common import func_json_response, abe_to_eas_fields_query, api_lookup_request

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for abe/lookup """

    logging.info('ABE Lookup processed a request.')

    try:
        params  = req.params.copy()
        return api_lookup_request(os.getenv('ABE_API_URL'), abe_to_eas_fields_query, params)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("ABE Lookup error occurred: %s", err)
        return func.HttpResponse(f"This endpoint encountered an error. {err}", status_code=500)
