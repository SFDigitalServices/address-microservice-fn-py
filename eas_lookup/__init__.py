""" eas/lookup init file """

import os
import json
import logging
import requests
import azure.functions as func
from shared_code.common import func_json_response


def main(req: func.HttpRequest) -> func.HttpResponse:
    """main function for eas/lookup"""

    logging.info("EAS Lookup processed a request.")

    try:
        params = req.params.copy()
        if "search" in params:
            search_param = params["search"]
            params["$where"] = (
                f"address like upper('{search_param}%') AND parcel_number IS NOT NULL"
            )
            del params["search"]

        response = requests.get(
            os.getenv("EAS_API_URL"),
            params=params,
            headers={"X-App-Token": os.getenv("ADDRESS_SVC_APP_TOKEN")},
            timeout=600,
        )

        cache_max_age = os.getenv("ADDRESS_SVC_CACHE_MAX_AGE")
        headers = {
            "Cache-Control": f"s-maxage=1, stale-while-revalidate, max-age={cache_max_age}",
            "Access-Control-Allow-Origin": "*",
        }

        return func_json_response(response, headers)

    # pylint: disable=broad-except
    except Exception as err:
        logging.error("EAS Lookup error occurred: %s", err)
        return func.HttpResponse(
            f"This endpoint encountered an error. {err}", status_code=500
        )
