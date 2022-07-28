""" avs/lookup init file """
import os
import logging
import azure.functions as func
from shared_code.common import func_json_response, avs_to_eas_fields_query, api_lookup_request

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for avs/lookup """

    logging.info('AVS Lookup processed a request.')

    try:
        params  = req.params.copy()
        return api_lookup_request(os.getenv('AVS_API_URL'), avs_to_eas_fields_query, params)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("AVS Lookup error occurred: %s", err)
        return func.HttpResponse(f"This endpoint encountered an error. {err}", status_code=500)
