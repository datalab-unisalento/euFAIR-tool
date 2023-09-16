import json

import ext_point
import settings


def F1(payload, link):
    permalinks = settings.load_permalink()

    max_point = 1
    scored_point = 0
    for distribution in payload["result"]["resources"]:
        if ("download_url" in distribution and link in distribution["download_url"]) or ("access_url" in distribution and link in distribution["access_url"]):
            for permalink in permalinks:
                if json.dumps(distribution).find(permalink) != -1:
                    scored_point += 1

    return max_point, scored_point


def F2(payload, link,  method):
    properties = settings.load_metadata_properties_raw(method, "distributions")
    max_point=0
    scored_point=0

    for distribution in payload["result"]["resources"]:
        if ("download_url" in distribution and link in distribution["download_url"]) or ("access_url" in distribution and link in distribution["access_url"]):
            for property_ in properties.keys():
                max_point += properties[property_]
                if property_ in distribution and distribution[property_] is not None:
                    print(scored_point, properties[property_])
                    scored_point += properties[property_]

    return max(1,max_point), scored_point


def F4(link):
    max_point = 1
    scored_point = 0

    print("LOG: searching indexing for " + link)
    if  ext_point.duckduckgo_indexed(link):
        print("LOG: indexing found")
        scored_point += 1

    return max_point, scored_point

# NUMBER OF NULL VALUES SET AS ASPECIFC BUT NEEDS TO BE IMPLEMENTED IN THE FILE
