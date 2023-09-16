import json
import re

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

    max_point = 1
    scored_point = 0
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
        mprint("LOG: is independent always pass for dataset obtained from dati.gov.it")
    else:
        reporter.add_to_report("--L'esistenza dei metadati è dipendente da quella dei dati.")

    return max_point, scored_point


def guidelines_a(payload):
    reporter.add_to_report("-GUIDELINES")

    payload_text = json.dumps(payload)
    max_point = 1
    point_scored = 0
    mprint("LOG: evaluating DATA QUALITY GUIDELINES for criteria A")

    if payload_text.find('"resources"') == -1 and payload_text.find('"distributions"') == -1:
        reporter.add_to_report("--la proprietà distributions non sembra essere implementata. "
                               "Impossibile trovare informazioni sui dati")

    elif len(re.findall('"resources?" : \[.*]')) == 1:
        distributions = re.findall('"resources?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored = distributions.count("download_url")
        if point_scored == 0:
            point_scored = distributions.count("access_url") / 2

    elif len(re.findall('"distributions?" : \[.*]')) == 1:
        distributions = re.findall('"distributions?" : \[.*]')[0]
        max_point = distributions.count('{')
        point_scored = distributions.count("download_url")
        if point_scored == 0:
            point_scored = distributions.count("access_url") / 2
            reporter.add_to_report("--la proprietà distributions non sembra avere implementato nessun download_url"
                                   "trovati access_url. punteggio dimezzato")

    return max_point, point_scored


