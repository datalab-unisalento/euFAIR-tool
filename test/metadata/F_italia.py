import copy
import inspect
import json
import ext_point
import log_and_error
import reporter
import settings


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

    except log_and_error.LoaderFileError:
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

    except log_and_error.LoaderFileError:
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


def F1(payload):
    reporter.add_to_report("-METRICA F1 ITALIA")
    max_point = 1
    mprint("LOG: F1->")
    mprint("LOG: finding resource permanent URL")
    point_scored = 0

    permalinks = settings.load_permalink()

    if "url" in payload["result"] and payload["result"]["url"]:

        for permalink in permalinks:
            if payload["result"]["url"].find(permalink) == -1:
                mprint("LOG: " + permalink + " permalink not found")

            else:
                mprint("LOG: " + permalink + " permalink found")
                point_scored = 1
                break

    elif "extras" in payload["result"]:
        for extra in payload["result"]["extras"]:
            if extra["key"] == "uri":
                for permalink in permalinks:
                    if extra["value"].find(permalink) == -1:
                        mprint("LOG: " + permalink + " permalink not found")
                    else:
                        mprint("LOG: " + permalink + " permalink found")
                        point_scored = 1
                        break

    if point_scored == 0:
        reporter.add_to_report("--I metadati non sembrano avere un permalink")

    mprint(f"LOG: F1 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


def F2(payload, method="merged"):
    reporter.add_to_report("-METRICA F2")
    mprint("LOG: F2->")
    try:
        prop_with_sub = settings.load_sup_link()
        prop_points = settings.load_point("result", method)
        schema_properties = settings.load_metadata_properties_schema(method)

        new_payload = copy.deepcopy(payload)

        if "resources" in new_payload["result"]:
            new_payload["result"]["distributions"] = new_payload["result"].pop("resources")

        metadata_properties = normalizer(new_payload["result"])

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
                    weight = find_weight(new_payload, _property, method)
                    print("LOG: " + _property + " has weight: " + str(weight))
                print("-points: " + str(prop_points[_property]) + " weight: " + str(weight))
                point_scored += round(prop_points[_property] * weight, 2)
            else:
                print("-" + _property + " not found or empty")
                reporter.add_to_report("--la proprietà " + _property + " non sembra essere stata dichiarata")

        mprint(f"LOG: F2 -> max point = {max_point} | point scored = {point_scored}")

        return max_point, point_scored

    except log_and_error.LoaderFileError:
        raise


def F3(payload):
    reporter.add_to_report("-METRICA F3")
    mprint("F3->")

    if "resources" not in payload["result"] or len(payload["result"]["resources"]) == 0:
        reporter.add_to_report("--la proprietà distributions non sembra essere implementata. "
                               "Impossibile trovare informazioni sui dati")
        return 1, 0

    max_point = len(payload["result"]["resources"])
    point_scored = 0

    mprint("LOG: found " + str(len(payload["result"]["resources"])) + " distributions")
    for idx, distribution in enumerate(payload["result"]["resources"]):
        if distribution["id"] is not None:
            mprint("LOG: for distribution " + str(idx + 1) + " found id: " + str(distribution["id"]))
            point_scored += 1
        else:
            reporter.add_to_report("--la distribuzione " + str(idx + 1) + " non sembra avere id")

    mprint(f"LOG: F3 -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored


def F4(payload, caller):
    reporter.add_to_report("-METRICA F4")
    mprint("F4->")
    max_point = 1
    point_scored = 0

    print("LOG: searching indexing")

    try:
        if caller:
            if "url" in caller["result"]:
                if ext_point.duckduckgo_indexed(
                        caller["result"]["url"]):
                    mprint("LOG: found indexing for permalink")
                    point_scored += 1

            elif 'extras' in caller["result"]:
                for extra in caller["result"]["extras"]:
                    if extra["key"] == "uri":
                        if ext_point.duckduckgo_indexed(
                                caller["result"]["url"]):
                            mprint("LOG: found indexing for permalink")
                            point_scored += 1

            return max_point, point_scored
        else:
            if ext_point.duckduckgo_indexed(f"https://www.dati.gov.it/view-dataset/dataset?id={payload['result']['id']}"):
                mprint("LOG: found indexing for permalink")
                point_scored += 1

        if point_scored == 0:
            reporter.add_to_report("--La risorsa non sembra indicizzata")

        mprint(f"LOG: F4 -> max point = {max_point} | point scored = {point_scored}")

        return max_point, point_scored

    except Exception as e:
        print("ERROR: duckduckgo not working")
        log_and_error.stack_up(e, inspect.currentframe())
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

    text = json.dumps(payload)

    if '"keywords"' in text:
        point_scored += 1
        mprint("LOG: keywords found")

    else:
        mprint("LOG: keywords not found")
        reporter.add_to_report("--la proprietà keywords non sembra essere assegnata")

    if '"categories"' in text:
        point_scored += 1
        mprint("LOG: categories found")
    else:
        print("LOG: categories not found")
        reporter.add_to_report("--la proprietà categories non sembra essere assegnata")

    if '"temporal"' in text:
        point_scored += 1
        mprint("LOG: temporal found")
    else:
        mprint("LOG: temporal not found")
        reporter.add_to_report("--la proprietà temporal non sembra essere assegnata")

    if '"spatial"' in text:
        point_scored += 1
        mprint("LOG: spatial found")
    else:
        print("LOG: spatial not found")
        reporter.add_to_report("--la proprietà spatial non sembra essere assegnata")

    mprint(f"LOG: F GUIDELINES -> max point = {max_point} | point scored = {point_scored}")

    return max_point, point_scored
