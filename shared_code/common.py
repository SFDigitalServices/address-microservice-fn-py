""" Common shared functions """
import re
import json
import jsend
import azure.functions as func

def func_json_response(response, headers=None):
    """ json func_json_response """
    json_data = json.loads(response.text)

    if response.status_code == 200:
        func_response = json.dumps(jsend.success({"items": json_data}))
    else:
        func_response = json.dumps(json_data)

    func_status_code = response.status_code

    return func.HttpResponse(
        func_response,
        status_code=func_status_code,
        mimetype="application/json",
        headers=headers
    )

def abe_to_eas_fields_query(query_string):
    """ replace abe fields with EAS fields in query string"""
    #pylint: disable=line-too-long
    address_field = "trim(property_street_number || greatest(property_street_number_sfx, '') || ' ' || property_street_name ||  ' ' || property_street_sfx || ' ' || greatest(property_unit, '') || greatest(property_unit_sfx, '')) as address"
    subs = {
        "address" : address_field,
        "parcel_number" : "block || lot as parcel_number",
        "address_number" : "property_street_number",
        "address_number_suffix" : "property_street_number_sfx",
        "street_name" : "property_street_name",
        "street_type" : "property_street_sfx",
        "unit_number" : "greatest(property_unit, '') || greatest(property_unit_sfx, '') as unit_number",
        "zip_code" : "'' as zip_code"

    }
    for old, new in subs.items():
        query_string = re.sub(r"\b%s\b" % old,new,query_string)

    return query_string
