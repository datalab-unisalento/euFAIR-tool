import requests

import settings


def A1(distribution):
    accepted_formats = settings.load_accepted_formats()

    max_point = 0
    act_point_given = 0
    act_point_accessible = 0
    download_url = []
    access_url = []
    url_arr = []

    if "download_url" in distribution \
            and distribution["download_url"] != [] \
            and distribution["download_url"] is not None:

        if distribution["download_url"] is list:
            for url in distribution["download_url"]:
                if url.split(".")[-1] in accepted_formats:
                    download_url.append(url)
        elif distribution["download_url"] is str:
            if distribution["download_url"].split(".")[-1] in accepted_formats:
                download_url.append(distribution["download_url"])

                # if requests.get(url).status_code in range(200,300):
                #     print("working")
                #     act_point +=1
                #     break
                # else: print("not working")

    if "access_url" in distribution \
            and distribution["access_url"] != [] \
            and distribution["access_url"] is not None:

        if distribution["access_url"] is list:
            for url in distribution["access_url"]:
                if url.split(".")[-1] in accepted_formats:
                    access_url.append(url)
        elif distribution["access_url"] is str:
            if distribution["access_url"].split(".")[-1] in accepted_formats:
                access_url.append(distribution["access_url"])
            #     print("access url seems file -> taken as download url")
            #     if requests.get(url).status_code in range (200, 299):
            #         print("working")
            #         act_point += 0.5
            #         break

            # else: print("not working")
    if "url" in distribution \
            and distribution["url"] != [] \
            and distribution["url"] is not None:
        if distribution["url"] is list:
            for url in distribution["access_url"]:
                if url.split(".")[-1] in accepted_formats:
                    url_arr.append(url)
        elif distribution["url"] is str:
            if distribution["url"].split(".")[-1] in accepted_formats:
                url_arr.append(distribution["access_url"])

    if download_url == [] and access_url == [] and url_arr == []:
        return 1, 0

    same_file_url = {}
    for url in download_url + access_url + url_arr:
        if url.split("/")[-1].split(".")[0] not in same_file_url:
            same_file_url[url.split("/")[-1].split(".")[0]] = [url]
        else:
            same_file_url[url.split("/")[-1].split(".")[0]].append(url)

    max_point += len(same_file_url.keys())

    for file in same_file_url:
        found = 0
        for url in same_file_url[file]:
            if url in download_url:
                act_point_given += 1
                found = 1
                break
        if found == 0:
            act_point_given += 0.5

        for url in same_file_url[file]:
            if url in download_url:
                if requests.get(url).status_code in range(200, 299):
                    act_point_accessible += 1
                    break

            elif url in access_url:
                if requests.get(url).status_code in range(200, 299):
                    act_point_accessible += 0.5
                    break

    scored_point = act_point_accessible + act_point_given

    return max_point, scored_point


def A1_1_():
    return 1, 0


def A1_2_():
    return 1, 0



