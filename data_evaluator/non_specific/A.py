import re

import requests


def A1(link):
    max_point = 0
    scored_point = 0

    max_point += 1

    is_ip = re.search(re.compile(
        r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b",
        re.IGNORECASE), link)

    is_url = re.match(re.compile(
        r"([A-Za-z0-9]+(\.[A-Za-z0-9]+)+)/[A-Za-z0-9]", re.IGNORECASE), link)

    if is_ip:
        print("LOG: identifier seems IP")
        scored_point += 1

    elif is_url:
        print("LOG: identifier seems URL")
        scored_point += 1

    if is_url or is_ip:
        if link.find("//") == -1:
            try:
                if requests.get(link).status_code in range(200,300):
                    link = "https://" + link

            except requests.exceptions.MissingSchema:
                print("WARNING: can't find the protocol")

            except:
                print("ERROR: CONNECTION ERROR")

        max_point += 1
        known_protocols = ["http", "https", "ftp", "tftp"] # protocol know to be open free and universally implementable
        is_known_protocol = re.match(re.compile(rf"({'|'.join(known_protocols)})://", re.IGNORECASE), link)

        if is_known_protocol:
            print("LOG: identifier use open and free protocol")
            scored_point += 1

        else:
            print("LOG: identifier does not use a standard protocol")

    return max_point, scored_point


def A1_1():
    return 1, 1


def A1_2():
    return 1, 1
