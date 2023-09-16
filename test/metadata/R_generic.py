import json
import re

import requests

import ext_point
import log
import reporter
import settings
from utility.utility import myprint as mprint


def community_standard(dataset_id):
    max_score = 405
    score = ext_point.mqa.retrieve_mqa_point(dataset_id)
    mprint("LOG: max score: " + str(max_score) + " | score: " + str(score))
    return score / max_score


def R1():
    reporter.add_to_report("-METRICA R1")

    max_point = 1
    scored_point = 0
    mprint("LOG: doesn't pass for generic")
    return max_point, scored_point


def R1_1(payload):
    reporter.add_to_report("-METRICA R1.1")

    mprint("LOG: searching for license in metadata")
    vocabularies = settings.load_vocabularies()

    max_point = 0
    point_scored = 0
    payload_text = json.dumps(payload)

    if payload_text.find('"resources"') == -1 and payload_text.find('"distributions"') == -1:
        reporter.add_to_report("--la proprietà distributions non sembra essere implementata. "
                               "Impossibile trovare informazioni sui dati")

    elif len(re.findall('"resources?" : \[.*]')) == 1:
        distributions = re.findall('"resources?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored += distributions.count("license")

        for property_ in vocabularies:
            for format_ in property_:
                point_scored += distributions.count(format_)

    elif len(re.findall('"distributions?" : \[.*]')) == 1:
        distributions = re.findall('"distributions?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored = distributions.count("license")

        for property_ in vocabularies:
            for format_ in property_:
                point_scored += distributions.count(format_)

    return max_point, point_scored


def R1_2(payload):
    reporter.add_to_report("-METRICA R1.2")

    max_point = 0
    scored_point = 0

    mprint("LOG: searching for provenance in metadata")
    max_point += 1

    payload_text = json.dumps(payload)
    if payload_text.find('"provenance"') != -1:
        scored_point += 1
    elif payload_text.find('"publisher"'):
        scored_point += 0.5
        reporter.add_to_report("--publisher implemented and taken as provenance but provenance not . half points")
    else:
        reporter.add_to_report("--provenance not implemented")

    return max_point, scored_point


def R1_3(payload):
    reporter.add_to_report("-METRICA R1.3")

    max_point = 0
    scored_point = 0

    max_point += 1
    mprint("LOG: finding data.europa.eu score")
    community_score = community_standard(payload)
    scored_point += community_score

    if scored_point<max_point:
        reporter.add_to_report("--see community guidelines")

    return max_point, scored_point


def guidelines_r(payload):  # TO IMPLEMENT SHACL VLIDATIO SEE GUIDELINES
    reporter.add_to_report("-GUIDELINES")

    max_point = 0
    scored_point = 0

    max_point += 1
    mprint("LOG: compliance to community standard always true for data.europe.eu")
    scored_point += 1

    mprint("LOG: searching for size in metadata")
    max_point += 1

    payload_text = json.dumps(payload)
    if payload_text.find('"byte_size"') != -1:
        scored_point += 1
    elif payload_text.find('"size"'):
        scored_point += 0.5
        reporter.add_to_report("--size implemented and taken as byte_size but byte_size not . half points")
    else:
        reporter.add_to_report("--byte_size not implemented")

    return max_point, scored_point
