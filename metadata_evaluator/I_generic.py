import json
import re
import time

import requests
from validate_utf8 import find_utf8_errors

from utility.utility import myprint as mprint

import reporter
import settings


def validate_utf8(dataset_id):
    try:
        errors = find_utf8_errors(requests.get(f"https://data.europa.eu/api/hub/search/datasets/{dataset_id}").content)
        if not errors:
            mprint("LOG: UTF-8 codec validated")
            return 1
        else:
            mprint("LOG: UTF-8 codec not validated")

        return 0
    except:
        return 0

def I1():
    reporter.add_to_report("-METRICA I1")

    max_point = 1
    scored_point = 0
    mprint("LOG: not a formal language")
    return max_point, scored_point


def I2(payload):
    reporter.add_to_report("-METRICA I2")

    vocabularies = settings.load_vocabularies()

    temp_max_point = 0
    for vocabulary in vocabularies:
        temp_max_point += len(vocabularies[vocabulary]["property"])

    max_point = max(temp_max_point, 1)

    # for _property in vocabularies:
    #     max_point += len(vocabularies[_property]["property"])

    payload_text = json.dumps(payload)


    scored_point = 0
    for _property in vocabularies:
        for format_ in vocabularies[_property]["vocabulary_format"]:
            if payload_text.find(format_) != -1:
                scored_point +=1
                break

    if scored_point == 0:
        reporter.add_to_report(f"--database doesn't seem to use vocabulary")

    return max_point, scored_point

def I3(payload, dataset_url):
    reporter.add_to_report("-METRICA I3")

    scored_point = 0
    text_payload = json.dumps(payload)

    url_found = re.findall(r'(https?://\S+)', text_payload)
    unique_url = []
    max_point = 1
    if url_found:
        for url in url_found:
            print(url)
            unique_url.append(url.split("//")[1].split("/")[0].split('"')[0].split(")")[0])
        max_point = len(url_found)
        unique_url = set(unique_url)

        mprint("LOG: found " + str(len(url_found)) + " url")

        dataset_url = dataset_url.split("//")[1].split("/")[0].split('"')[0].split(")")[0]
        for url in unique_url:
            if url.find(dataset_url) == -1:
                mprint("LOG: external link: " + url)
                scored_point += 1

        reporter.add_to_report(f"--of {len(url_found)} only {scored_point} refer to outside of domain")

    else:
        mprint("LOG: no URL found ")

    return max_point, scored_point


def guidelines_i(dataset_id):
    reporter.add_to_report("-GUIDELINES")

    max_point = 1
    point_scored = 0

    if validate_utf8(dataset_id):
        point_scored += 1

    else:
        reporter.add_to_report("--UTF-8 validation not passed")

    return max_point, point_scored
