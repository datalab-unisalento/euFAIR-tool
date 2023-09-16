import inspect
import json
import ext_point

import settings
from reporter import reporter
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
from log.error import error


# come per find_weight ma per sottoproprietà che hanno sotto-sotto-proprietà
def find_sub_weight(payload, property_, sub_property, method):
    try:
        print("--> calculating weight of " + sub_property)
        prop_points = settings.load_point(sub_property, method)
        link_in_prop = settings.load_relation()
        metadata_properties = payload["result"]

        max_point = settings.load_max_point(sub_property, method)
        if max_point == 0:
            return 1

        act_point = 0
        for sub_sub_property in link_in_prop[sub_property]:
            if sub_sub_property in metadata_properties[property_][sub_property] \
                    and metadata_properties[property_][sub_property] != {} \
                    and metadata_properties[property_][sub_property] is not None:
                act_point += prop_points[sub_sub_property]

        weight = act_point / max_point

        print("-->LOG: sub_weight = " + str(weight))

        return weight

    except settings.LoaderFileError:
        raise


# Se una proprietà ha sottoproprietà allora il punteggio che otterrà dipendera
# da quanto siano complete le sue sottoproprietà
# se le sue sottoproprietà ottenessero un punteggio dell'80% di completezza allora
# la proprietà prendera il suo punteggio moltiplicato per il peso delle sottoproprietà quindi 0.8
def find_weight(payload, _property, method):
    try:
        print("->LOG: calculating weight of " + str(_property))
        prop_with_sub = settings.load_sup_link()
        prop_points = settings.load_point(_property, method)
        link_in_prop = settings.load_relation()
        metadata_properties = payload["result"]

        max_point = round(settings.load_max_point(_property, method), 2)
        if max_point == 0:
            return 1

        act_point = 0

        sub_weight = 1
        for sub_property in link_in_prop[_property]:
            if sub_property in metadata_properties[_property] \
                    and metadata_properties[_property][sub_property] != {} \
                    and metadata_properties[_property][sub_property] is not None:

                if sub_property in prop_with_sub:
                    print("--> LOG: " + sub_property + " seems to have sub -> ")
                    sub_weight = find_sub_weight(payload, _property, sub_property, method)

                act_point += round(sub_weight * prop_points[sub_property], 2)

            else:
                print("-->LOG: " + sub_property + " not found or empty")

        weight = round(sub_weight * (act_point / max_point), 2)

        print("->LOG: weight = " + str(weight))

        return weight

    except settings.LoaderFileError:
        raise


# alcune proprietà sono multivalore, ai fini della richness e della completezza
# verrà considerata la presenza di almeno una come positiva
# la presenza di ulteriori valori oltre al primo verrà ignorata
# dato il payload restitutisce il payload come se tutte le proprietà multivalore avessero un solo valore
def normalizer(my_obj):
    my_obj2 = json.dumps(my_obj)
    my_obj2 = json.loads(my_obj2)
    while type(my_obj2) is list:
        if my_obj2:
            my_obj2 = my_obj2[0]
        else:
            my_obj2 = None

    if type(my_obj2) is not list and type(my_obj2) is not dict:
        return my_obj2

    for _property in my_obj2:
        my_obj2[_property] = normalizer(my_obj2[_property])

    return my_obj2


# F1. Metadata are assigned a globally unique and persistent identifier
# Nei metadata forniti da hub-search (data.europa.eu) il permalink della risorsa è inserito nel campo "resource"
# Teoricamente qualsiasi dataset recuperato da data.europa.eu dovrebbe esserne fornito
# La proprietà viene comunque controllata verificando che il campo sia presente, non sia vuoto \
# e il link al suo interno sia un permalink
# Il link viene quindi confrontato con dei permalink riconosciuti inseriti in settings/permanent_link.json
def F1(payload):
    reporter.add_to_report('METRICA F1:')
    max_point = 1
    mprint("LOG: F1->", bc.CYAN)
    mprint("LOG: finding resource permanent URL")
    point_scored = 0

    if "resource" in payload["result"] \
            and payload["result"]["resource"] is not None:

        permalinks = settings.load_permalink()

        for permalink in permalinks:
            if payload["result"]["resource"].find(permalink) == -1:
                mprint("LOG: " + permalink + " permalink not found")

            else:
                mprint("LOG: " + permalink + " permalink found")
                point_scored = 1
                break

        if point_scored == 0:
            reporter.add_to_report("--I metadati non sembrano avere un permalink")

        mprint(f"LOG: F1 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


# La struttura del file properties_settings permette d'implementare più profili di meta datazione \
# con la relativa obbligatorietà delle proprietà
# Sono nativamente implementati i profili DCAT_AP e DCAT_AP-IT
# Viene automaticamente implementato il profilo merged che considera \
# la più alta obbligatorietà tra tutti i profili inseriti
# F2. Data are described with rich metadata (defined by R1 below)
def F2(payload, method="merged"):
    reporter.add_to_report("-METRICA F2")
    mprint("LOG: F2->")
    try:
        prop_with_sub = settings.load_sup_link()
        prop_points = settings.load_point("result", method)
        schema_properties = settings.load_metadata_properties_schema(method)

        metadata_properties = normalizer(payload["result"])

        max_point = settings.load_max_point("result", method)

        point_scored = 0

        mprint("LOG: evaluating properties, see console for more info")
        for _property in schema_properties:
            print("LOG: evaluating " + str(_property))
            weight = 1

            if _property in metadata_properties and metadata_properties[_property] != {} \
                    and metadata_properties[_property] is not None:
                if _property in prop_with_sub:
                    print("->LOG: " + _property + " seems to have sub -> ")
                    weight = find_weight(payload, _property, method)
                    print("LOG: " + _property + " has weight: " + str(weight))
                print("-points: " + str(prop_points[_property]) + " weight: " + str(weight))
                point_scored += round(prop_points[_property] * weight, 2)
            else:
                print("-" + _property + " not found or empty")
                reporter.add_to_report("--la proprietà " + _property + " non sembra essere stata dichiarata")

        mprint(f"LOG: F2 -> max point = {max_point} | point scored = {point_scored}")

        return max_point, point_scored

    except settings.LoaderFileError:
        raise


# F3. Metadata clearly and explicitly include the identifier of the data it describes
def F3(payload):
    reporter.add_to_report("-METRICA F3")
    mprint("F3->")

    if "distributions" not in payload["result"] or len(payload["result"]["distributions"]) == 0:
        reporter.add_to_report("--la proprità distributions non sembra essere implementata. "
                               "Impossibile torvare informazioni sui dati")
        return 1, 0

    max_point = len(payload["result"]["distributions"])
    point_scored = 0

    mprint("LOG: found " + str(len(payload["result"]["distributions"])) + " distributions")
    for idx, distribution in enumerate(payload["result"]["distributions"]):
        if distribution["id"] is not None:
            mprint("LOG: for distribution " + str(idx + 1) + " found id: " + str(distribution["id"]))
            point_scored += 1
        else:
            reporter.add_to_report("--la distribuzione " + str(idx + 1) + " non sembra avere id")

    mprint(f"LOG: F3 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


# F4. Metadata are registered or indexed in a searchable resource
def F4(payload):
    reporter.add_to_report("-METRICA F4")
    mprint("F4->")
    max_point = 1
    point_scored = 0

    print("LOG: searching indexing")

    try:
        if ext_point.duckduckgo_indexed(payload["result"]["resource"]):
            mprint("LOG: found indexing for permalink")
            point_scored += 1

        elif ext_point.duckduckgo_indexed(f'https://data.europa.eu/api/hub/search/datasets/{payload["result"]["id"]}'):
            mprint("LOG: found indexing for link")
            point_scored += 1

        else:
            reporter.add_to_report("--La risorsa non sembra indicizzata")

        mprint(f"LOG: F4 -> max point = {max_point} | point scored = {point_scored}")

        return max_point, point_scored

    except Exception as e:
        print("ERROR: duckduckgo not working")
        error(e, inspect.currentframe())
        return max_point, 0


def guidelines_f(payload):
    mprint("-GUIDELINES->")
    reporter.add_to_report("-GUIDELINES")
    print("LOG: evaluating DATA QUALITY GUIDELINES for criteria F")
    max_point = 15
    point_scored = 0

    empty_fields = 0
    payload_text = json.dumps(payload)
    fields = payload_text.count('": "') + payload_text.count('": [') + payload_text.count('": {')
    empty_fields += payload_text.count("null")
    empty_fields += payload_text.count("[]")
    empty_fields += payload_text.count("{}")
    mprint("LOG: found " + str(empty_fields) + " empty fields : " + str(round(empty_fields / fields * 100, 2)) + "%")
    point_scored += (fields - empty_fields) / fields * 10

    if "keywords" in payload["result"] and payload["result"]["keywords"]:
        point_scored += 1
        mprint("LOG: keywords found")

    else:
        mprint("LOG: keywords not found")
        reporter.add_to_report("--la proprietà keywords non sembra essere assegnata")

    if "categories" in payload["result"] and payload["result"]["categories"]:
        point_scored += 1
        mprint("LOG: categories found")
    else:
        print("LOG: categories not found")
        reporter.add_to_report("--la proprietà categories non sembra essere assegnata")

    if "temporal" in payload["result"] and payload["result"]["temporal"]:
        point_scored += 1
        mprint("LOG: temporal found")
    else:
        mprint("LOG: temporal not found")
        reporter.add_to_report("--la proprietà temporal non sembra essere assegnata")

    if "spatial" in payload["result"] and payload["result"]["spatial"]:
        point_scored += 1
        mprint("LOG: spatial found")
    else:
        print("LOG: spatial not found")
        reporter.add_to_report("--la proprietà spatial non sembra essere assegnata")

    mprint(f"LOG: F GUIDELINES -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored
