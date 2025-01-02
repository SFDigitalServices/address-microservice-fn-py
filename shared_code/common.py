""" Common shared functions """

import os
import re
import json
import jsend
import requests
import azure.functions as func


def func_json_response(response, headers=None, json_root="items"):
    """json func_json_response"""
    json_data = json.loads(response.text)
    func_status_code = response.status_code

    if response.status_code == 200:
        func_response = {json_root: json_data}
    else:
        func_response = json_data

    return func_jsend_response(
        func_response, headers=headers, status_code=func_status_code
    )


def func_jsend_response(data, headers=None, status_code=200):
    """func_jsend_success_response"""
    if 200 <= status_code < 500:
        # check if data is JSON, else wrap in "message"
        try:
            # jsend: data must be the dict type
            if not isinstance(data, dict):
                data = json.loads(data)
        except (TypeError, ValueError) as _err:
            data = {"json": data}
        if 200 <= status_code < 300:
            func_response = json.dumps(jsend.success(data))
        else:
            func_response = json.dumps(jsend.fail(data))
    else:
        func_response = json.dumps(jsend.error(data))

    return func.HttpResponse(
        func_response,
        status_code=status_code,
        mimetype="application/json",
        headers=headers,
    )


def abe_to_eas_fields_query(query_string):
    """replace abe fields with EAS fields in query string"""
    # pylint: disable=line-too-long
    address_field = "trim(property_street_number || greatest(property_street_number_sfx, '') || ' ' || property_street_name ||  ' ' || property_street_sfx || ' ' || greatest(property_unit, '') || greatest(property_unit_sfx, '')) as address"
    subs = {
        "address": address_field,
        "parcel_number": "block || lot as parcel_number",
        "address_number": "property_street_number as address_number",
        "address_number_suffix": "property_street_number_sfx as address_number_suffix",
        "street_name": "property_street_name as street_name",
        "street_type": "property_street_sfx as street_type",
        "unit_number": "greatest(property_unit, '') || greatest(property_unit_sfx, '') as unit_number",
        "zip_code": "'' as zip_code",
    }
    for old, new in subs.items():
        # pylint: disable=consider-using-f-string
        query_string = re.sub(r"\b%s\b" % old, new, query_string)

    return query_string


def avs_to_eas_fields_query(query_string):
    """replace abe fields with AVS fields in query string"""
    # pylint: disable=line-too-long
    address_field = "trim(street_number || greatest(street_number_sfx, '') ||  ' ' || avs_street_name ||  ' ' || avs_street_sfx || ' ' || greatest(unit, '')) as address"
    subs = {
        "address": address_field,
        "parcel_number": "block || lot as parcel_number",
        "address_number": "street_number as address_number",
        "address_number_suffix": "street_number_sfx as address_number_suffix",
        "street_name": "avs_street_name as street_name",
        "street_type": "avs_street_sfx as street_type",
        "unit_number": "greatest(unit, '') as unit_number",
    }
    for old, new in subs.items():
        # pylint: disable=consider-using-f-string
        query_string = re.sub(r"\b%s\b" % old, new, query_string)

    return query_string


def error_response(err):
    """return error response"""
    msg_error = f"This endpoint encountered an error. {err}"
    func_response = json.dumps(jsend.error(msg_error))
    return func.HttpResponse(func_response, status_code=500)


def api_json_request(api_url, field_mapping_function, params):
    """make json api request"""
    if "format" in params:
        if params["format"] == "eas":
            if (
                "$where" in params
                and "parcel_number" in params["$where"]
                and (
                    "$select" not in params or "parcel_number" not in params["$select"]
                )
            ):
                params["$select"] += ",parcel_number"
            if "$select" in params:
                params["$select"] = field_mapping_function(params["$select"])
        del params["format"]
    response = requests.get(
        api_url,
        params=params,
        headers={
            "Authorization": "Basic " + os.getenv("ADDRESS_SVC_AUTH_API_KEY"),
            "X-App-Token": os.getenv("ADDRESS_SVC_APP_TOKEN"),
        },
        timeout=600,
    )
    print(params)
    headers = {"Access-Control-Allow-Origin": "*"}
    return func_json_response(response, headers)


def api_lookup_request(api_url, field_mapping_function, params):
    """make search api request"""
    if "search" in params:
        search_param = params["search"]
        params["$where"] = (
            f"address like upper('{search_param}%') AND block IS NOT NULL and lot IS NOT NULL"
        )
        if "$select" in params:
            params["$select"] = field_mapping_function(params["$select"])
        else:
            params["$select"] = field_mapping_function("address")
        del params["search"]

    response = requests.get(
        api_url,
        headers={
            "Authorization": "Basic " + os.getenv("ADDRESS_SVC_AUTH_API_KEY"),
            "X-App-Token": os.getenv("ADDRESS_SVC_APP_TOKEN"),
        },
        params=params,
        timeout=600,
    )
    cache_max_age = os.getenv("ADDRESS_SVC_CACHE_MAX_AGE")
    headers = {
        "Cache-Control": f"s-maxage=1, stale-while-revalidate, max-age={cache_max_age}",
        "Access-Control-Allow-Origin": "*",
    }

    return func_json_response(response, headers)
