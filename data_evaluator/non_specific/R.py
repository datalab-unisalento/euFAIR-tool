# APPROPIATE AMOUNT OF DATA  SET AS ASPECIFIC  BUT NEEDS TO BE IMPLEMENTED IN THE FILE
# FREENESS FROM DUPLICATES  SET AS ASPECIFIC  BUT NEEDS TO BE IMPLEMENTED IN THE FILE
import json

import requests

import data_retriever
import settings


def R1_1(payload, link):
    vocabularies = settings.load_vocabularies()
    max_point = 0
    scored_point = 0

    for distribution in payload["result"]["resources"]:
        if ("download_url" in distribution and link in distribution["download_url"]) or ("access_url" in distribution and link in distribution["access_url"]):
            max_point += 2
            if "license" in distribution and distribution["license"] is not None:
                scored_point += 1
                print("LOG:license found")
                if distribution["license"] == vocabularies["license"]["vocabulary_format"][
                                              :len(distribution["license"])] \
                        and requests.get(distribution["license"]).status_code in range(200, 400):
                    print("LOG: license respect vocabulary")
                    scored_point += 1
                else:
                    print("LOG: license does not respect vocabulary")

    max_point=max(max_point, 1)
    return max_point, scored_point


def R1_2(payload, link):
    max_point = 0
    scored_point = 0

    for distribution in payload["result"]["resources"]:
        if ("download_url" in distribution and link in distribution["download_url"]) or (
                "access_url" in distribution and link in distribution["access_url"]):
            max_point += 1
            if "provenance" in distribution and distribution["provenance"] is not None:
                print("LOG: provenance found")
                scored_point += 1

    return max(1, max_point), scored_point


def R1_3(id_europa):

    #         community_metrics = json.dumps(data_retriever.retrieve_distribution_metrics(payload["result"]["id"], distribution["id"]))
    #
    #         good = community_metrics.count("true") + community_metrics.count("200")
    #         print("LOG: find " + str(good) + " good community metrics")
    #         bad = community_metrics.count("{}") + community_metrics.count("false")
    #         print("LOG: find " + str(bad) + " bad community metrics")
    #
    #         scored_point += good/ (good + bad)
    #
    #         return max_point, scored_point
    # return -1

    return 1, 0

