""" avs/json init file """
import os
import logging
import azure.functions as func
from shared_code.common import avs_to_eas_fields_query,error_response,api_json_request

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for abe/json """
    logging.info('AVS JSON processed a request.')

    try:
        params  = req.params.copy()
        return api_json_request(os.getenv('AVS_API_URL'), avs_to_eas_fields_query, params)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("AVS JSON error occurred: %s", err)
        return error_response(err)
