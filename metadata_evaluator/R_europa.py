import requests

from utility.utility import myprint as mprint
import reporter
import settings


def community_standard(payload):
    max_score = 405
    score = payload["result"]["quality_meas"]["scoring"]
    mprint("LOG: max score: " + str(max_score) + " | score: " + str(score))
    return score / max_score


def R1():
    reporter.add_to_report("-METRICA R1")

    max_point = 1
    scored_point = 1
    mprint("LOG: always pass for data europa")
    return max_point, scored_point


def R1_1(payload):
    reporter.add_to_report("-METRICA R1.1")

    mprint("LOG: searching for license in metadata")
    vocabularies = settings.load_vocabularies()

    max_point = 0
    scored_point = 0

    mprint("LOG: found " + str(len(payload["result"]["distributions"])) + " distributions")

    for idx, distribution in enumerate(payload["result"]["distributions"]):
        max_point += 2
        if "license" in distribution and distribution["license"] is not None:
            mprint("LOG: for distribution " + str(idx + 1) + " found license")
            scored_point += 1

            if distribution["license"] == vocabularies["license"]["vocabulary_format"][:len(distribution["license"])] \
                    and requests.get(distribution["license"]).status_code in range(200, 400):
                mprint("LOG: license respect vocabulary")
                scored_point += 1

            else:
                reporter.add_to_report("--license doesn't respect vocabulary")
        else:
            reporter.add_to_report("--license not found")

    return max_point, scored_point


def R1_2(payload):
    reporter.add_to_report("-METRICA R1.2")

    max_point = 0
    scored_point = 0

    mprint("LOG: searching for provenance in metadata")
    max_point += 1
    if "provenance" in payload["result"] and payload["result"]["provenance"] is not None:
        mprint("LOG: found provenance")
        scored_point += 1

    elif ("publisher" in payload["result"] and payload["result"]["publisher"] is not None) \
            or ("creator" in payload["result"] and payload["result"]["creator"] is not None):
        mprint("LOG: provenance not found, but found publisher/creator")
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
    for distribution in payload["result"]["distributions"]:
        if "byte_size" in distribution and distribution["byte_size"] is not None:
            mprint("LOG: size found")
            scored_point += 1
        else:
            reporter.add_to_report("--byte_size not implemented")

    return max_point, scored_point
