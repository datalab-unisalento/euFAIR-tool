import inspect
import json
import re

import ext_point
import log
import reporter
import settings

from utility.utility import myprint as mprint



def F1(payload, dataset_id):
    reporter.add_to_report("-METRICA F1 ITALIA")
    max_point = 1
    mprint("LOG: F1->")
    mprint("LOG: finding resource permanent URL")
    point_scored = 0

    permalinks = settings.load_permalink()

    payload = json.dumps(payload)

    for permalink in permalinks:
        if len(re.findall(permalink + ".*" + dataset_id, payload)) > 0:
            mprint("LOG: " + permalink + " permalink found")
            point_scored = 1
            break
        else:
            mprint("LOG: " + permalink + " permalink not found")

    reporter.add_to_report("--I metadati non sembrano avere un permalink")

    mprint(f"LOG: F1 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


def F2(payload, method="merged"):
    reporter.add_to_report("-METRICA F2")
    mprint("LOG: F2->")

    schema_properties = settings.load_metadata_properties_raw(method)
    prop_points = settings.load_point("result", method)

    max_point = settings.load_max_point("result", method)

    point_scored = 0

    payload = json.dumps(payload)

    mprint("LOG: evaluating properties, see console for more info")
    for _property in schema_properties:
        print("LOG: evaluating " + str(_property))

        if payload.find('"' + _property + '"') != -1:
            print("-property: " + _property + " found")
            point_scored += prop_points[_property]
        else:
            print("-" + _property + " not found")
            reporter.add_to_report("--la proprietà " + _property + " non sembra essere stata dichiarata")

        mprint(f"LOG: F2 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


def F3(payload):
    reporter.add_to_report("-METRICA F3")
    mprint("F3->")

    payload_text = json.dumps(payload)

    max_point = 1
    point_scored = 0

    if payload_text.find('"resources"') == -1 and payload_text.find('"distributions"') == -1:
        reporter.add_to_report("--la proprietà distributions non sembra essere implementata. "
                               "Impossibile trovare informazioni sui dati")

    elif len(re.findall('"resources?" : \[.*]')) == 1:
        distributions = re.findall('"resources?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored = distributions.count("id")

    elif len(re.findall('"distributions?" : \[.*]')) == 1:
        distributions = re.findall('"distributions?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored = distributions.count("id")

    mprint(f"LOG: F3 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


def F4(url):
    reporter.add_to_report("-METRICA F4")
    mprint("F4->")
    max_point = 1
    point_scored = 0

    print("LOG: searching indexing")

    try:
        if ext_point.duckduckgo_indexed(url):
            mprint("LOG: found indexing for permalink")
            point_scored += 1

        else:
            reporter.add_to_report("--La risorsa non sembra indicizzata")

        mprint(f"LOG: F4 -> max point = {max_point} | point scored = {point_scored}")

        return max_point, point_scored

    except Exception as e:
        print("ERROR: duckduckgo not working")
        log_and_error.stack_up(e, inspect.currentframe())
        return max_point, 0


def guidelines_f(payload):
    mprint("-GUIDELINES->")
    reporter.add_to_report("-GUIDELINES")
    print("LOG: evaluating DATA QUALITY GUIDELINES for criteria F")
    max_point = 6
    point_scored = 0

    empty_fields = 0
    payload_text = json.dumps(payload)
    fields = payload_text.count('": "') + payload_text.count('": [') + payload_text.count('": {') + 1
    empty_fields += payload_text.count("null")
    empty_fields += payload_text.count("[]")
    empty_fields += payload_text.count("{}")
    mprint(
        "LOG: found " + str(empty_fields) + " empty fields : " + str(round(empty_fields / fields * 100, 2)) + "%")
    point_scored += (fields - empty_fields) / fields


    if '"keywords"' in payload_text:
        point_scored += 1
        mprint("LOG: keywords found")

    else:
        mprint("LOG: keywords not found")
        reporter.add_to_report("--la proprietà keywords non sembra essere assegnata")

    if '"categories"' in payload_text:
        point_scored += 1
        mprint("LOG: categories found")
    else:
        print("LOG: categories not found")
        reporter.add_to_report("--la proprietà categories non sembra essere assegnata")

    if '"temporal"' in payload_text:
        point_scored += 1
        mprint("LOG: temporal found")
    else:
        mprint("LOG: temporal not found")
        reporter.add_to_report("--la proprietà temporal non sembra essere assegnata")

    if '"spatial"' in payload_text:
        point_scored += 1
        mprint("LOG: spatial found")
    else:
        print("LOG: spatial not found")
        reporter.add_to_report("--la proprietà spatial non sembra essere assegnata")

    mprint(f"LOG: F GUIDELINES -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored
