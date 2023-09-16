import json

import requests
import reporter
from utility.utility import myprint as mprint


def is_standard():
    return 1


def is_open():
    return 1


def is_free():
    return 1


def is_universal():
    return 1


def allows_authorization():
    return 0


def is_independent():  # metadata are retrievable even if data are not
    return 1


def A1():
    reporter.add_to_report("-METRICA A1")

    max_point=1
    scored_point=0
    if is_standard():
        scored_point += 1
        mprint("LOG: is standard always pass for url")
    else:
        reporter.add_to_report("--Il protocollo di recupero del dataset non sembra essere standard")

    return max_point, scored_point


def A1_1():
    reporter.add_to_report("-METRICA A1.1")

    max_point = 3
    scored_point = 0

    if is_open():
        scored_point += 1
        mprint("LOG: is open always pass for url")
    else:
        reporter.add_to_report("--Il protocollo di recupero del dataset non sembra essere aperto")
    if is_free():
        scored_point += 1
        mprint("LOG: is free always pass for url")
    else:
        reporter.add_to_report("--Il protocollo di recupero del dataset non sembra essere aperto")
    if is_universal():
        scored_point += 1
        mprint("LOG: is universal always pass for url")
    else:
        reporter.add_to_report("--Il protocollo di recupero del dataset non sembra essere universale")

    return max_point, scored_point


def A1_2():
    reporter.add_to_report("-METRICA A1.2")

    max_point = 1
    scored_point = 0

    if allows_authorization():
        scored_point += 0.5
        mprint("LOG: allows authorization always pass for url")
    else:
        reporter.add_to_report("--Il protocollo di recupero del dataset "
                               "non sembra consentire procedure di autenticazione")

    return max_point, scored_point


def A2():
    reporter.add_to_report("-METRICA A2")

    max_point = 1
    scored_point = 0

    if is_independent():
        scored_point += 1
        mprint("LOG: is independent always pass for data europa")
    else:
        reporter.add_to_report("--L'esistenza dei metadati è dipendente da quella dei dati.")

    return max_point, scored_point


def guidelines_a(payload):
    reporter.add_to_report("-GUIDELINES")

    mprint("LOG: evaluating DATA QUALITY GUIDELINES for criteria A")
    if "distributions" not in payload["result"] or payload["result"]["distributions"] == [1]:
        reporter.add_to_report("--la proprietà distributions non sembra essere implementata. "
                               "Impossibile trovare informazioni sui dati")
        return 1, 0

    max_point = len(payload["result"]["distributions"]) * 3
    mprint("LOG: found " + str(len(payload["result"]["distributions"])) + " distribution")
    scored_point = 0

    for idx, distribution in enumerate(payload["result"]["distributions"]):
        print("LOG: distribution " + str(idx + 1))
        if "download_url" in distribution \
                and distribution["download_url"] is not None \
                and distribution["download_url"] != []:
            print("LOG: found download url")
            scored_point += 1
            max_point_found = 0
            for url in distribution["download_url"]:
                try:
                    response = requests.get(url)
                    if response.status_code in range(200, 400) or response.status_code == 401:
                        print("LOG: url working")
                        max_point_found = max(1, max_point_found)
                        if response.status_code != 401:
                            print("LOG: url accessible")
                            max_point_found = max(2, max_point_found)
                            break
                    else:
                        print("LOG: url not accessible")

                except Exception as e:
                    print("ERROR: connection error in guidelines_a ->" + str(e))
            scored_point = max(scored_point, max_point_found)

            if max_point_found == 1:
                reporter.add_to_report("--per la distribuzione: " + distribution["id"] +
                                       " è fornito un url valido ma non accessibile")
            if max_point_found == 0:
                reporter.add_to_report("--per la distribuzione: " + distribution["id"] +
                                       " non è fornito un url valido")

        else:
            if "access_url" in distribution \
                    and distribution["access_url"] is not None \
                    and distribution["access_url"] != []:
                print("LOG: found access url")
                scored_point += 0.5
            max_point_found = 0
            for url in distribution["access_url"]:
                try:
                    response = requests.get(url)
                    if response.status_code in range(200, 400) or response.status_code == 401:
                        print("LOG: url working")
                        max_point_found = max(max_point_found, 0.5)
                        if response.status_code != 401:
                            print("LOG: url accessible")
                            max_point_found = max(1, max_point_found)
                            break
                    else:
                        print("LOG: url not accessible")

                except Exception as e:
                    print("ERROR: connection error in guidelines_a ->", e)

            if max_point_found == 0.5:
                reporter.add_to_report("--per la distribuzione: " + distribution["id"] +
                                       " è fornito un url valido ma non accessibile. "
                                       "L'URL sembra un access_url mentre dovrebbe essere download_url. "
                                       "Il punteggio verrà dimezzato")
            if max_point_found == 0:
                reporter.add_to_report("--per la distribuzione: " + distribution["id"] +
                                       " è fornito un url non valido.")

            else:
                reporter.add_to_report("--per la distribuzione: " + distribution["id"] +
                                       " è  fornito un url valido e accessibile ma segnalato in access_url. "
                                       "Se questo è un download_url va nella proprietà appropriata. "
                                       "Il punteggio verrà dimezzato")

        scored_point += max_point_found

    return max_point, scored_point
