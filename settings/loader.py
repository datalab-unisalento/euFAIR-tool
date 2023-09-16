import csv
import datetime
import inspect
import json
import pandas as pd
from log.error import error
from utility.utility import myprint as mprint
import settings

npath = "settings/settings_file/"

def load_txt_to_json(file):
    try:
        with open(file, "r") as file:
            json_ = json.loads(file.read())
        return json_

    except FileNotFoundError as e:
        print("ERROR: Property file not found in loading json")
        error(e, inspect.currentframe())
        raise LoaderFileError

    except IOError as e:
        print("ERROR: Can't open the settings files in loading json")
        error(e, inspect.currentframe())

        raise LoaderFileError

    except Exception as e:
        print("ERROR: Unexpected error:", e, type(e))
        error(e, inspect.currentframe())
        raise LoaderFileError
def load_json_read(file):
    try:
        with open(file, "r") as file:
            json_ = json.load(file)
        return json_

    except FileNotFoundError as e:
        print("ERROR: Property file not found in loading json")
        error(e, inspect.currentframe())
        raise LoaderFileError

    except IOError as e:
        print("ERROR: Can't open the settings files in loading json")
        error(e, inspect.currentframe())

        raise LoaderFileError

    except Exception as e:
        print("ERROR: Unexpected error:", e, type(e))
        error(e, inspect.currentframe())
        raise LoaderFileError

def write_json_read(file, to_write):
    try:
        with open(file, "w") as file:
            file.write(json.dumps(to_write))

        return

    except FileNotFoundError as e:
        print("ERROR: Property file not found in loading json")
        error(e, inspect.currentframe())
        raise LoaderFileError

    except IOError as e:
        print("ERROR: Can't open the settings files in loading json")
        error(e, inspect.currentframe())

        raise LoaderFileError

    except Exception as e:
        print("ERROR: Unexpected error:", e, type(e))
        error(e, inspect.currentframe())
        raise LoaderFileError


# CHECKED
# restituisce lo schema di tutte le proprietà insieme al loro peso nel metodo di valutazione scelto
# e l'elenco delle sottoproprietà che possiedono
# {nome_proprietà : { "point" : peso_della_proprietà , "sub" : elenco_sottoproprietà}
def load_metadata_properties_schema(method="merged"):
    mprint("LOG: loading schema of property - weight and sub property")
    try:
        properties = settings.load_json_read(npath + "properties_settings.json")

        schema = {}
        for property_ in properties["result"]:
            if method in property_:
                if property_["property"] not in list(properties.keys()):
                    schema[property_["property"]] = {"point": property_[method], "sub": None}
                else:
                    sub_properties = {}
                    for sub_property in properties[property_["property"]]:
                        if method in sub_property:
                            if sub_property["property"] not in list(properties.keys()):
                                sub_properties[sub_property["property"]] = {"point": sub_property[method], "sub": None}
                            else:
                                sub_sub_properties = {}
                                for sub_sub_property in properties[sub_property["property"]]:
                                    if method in sub_sub_property:
                                        sub_sub_properties[sub_sub_property["property"]] = {
                                            "point": sub_sub_property[method], "sub": None}
                                if sub_sub_properties != {}:
                                    sub_properties[sub_property["property"]] = {"point": sub_property[method],
                                                                                "sub": sub_sub_properties}

                    schema[property_["property"]] = {"point": property_[method],
                                                     "sub": sub_properties}
                    if sub_properties == {}:
                        schema[property_["property"]]["sub"] = None

        return schema

    except LoaderFileError:
        raise


def load_metadata_properties_raw(method="merged", propertyy="result"):
    mprint("LOG: loading schema of property - weight and sub property")
    try:
        properties = settings.load_json_read(npath + "properties_settings.json")

        new_prop = {}
        for property_ in properties[propertyy]:
            if method in property_:
                new_prop[property_["property"]] = calc_point(property_[method])
            else:
                new_prop[property_["property"]] = 0
        return new_prop

    except LoaderFileError:
        raise


def calc_point(value):
    match value:
        case 'M':
            return 1
        case 'R':
            return 0.5
        case 'O':
            return 0.2


# CHECKED
# restituisce un vocabolario {nome_proprietà: peso_della_proprietà} per il metodo di valutazione scelto
def load_point(sup, method="merged"):
    mprint("LOG: creating property-weight dictionary")
    try:
        properties = settings.load_json_read(npath + "properties_settings.json")

        point = {}
        for property_ in properties[sup]:
            if method in property_:
                point[property_["property"]] = calc_point(property_[method])
            else:
                point[property_["property"]] = 0

        return point

    except LoaderFileError:
        raise


# CHECKED
# data una proprietà restituisce i punti massimi che questa può ottenere
def load_max_point(sup, method):
    try:
        properties = settings.load_json_read(npath + "properties_settings.json")

        point = 0

        for property_ in properties[sup]:
            if method in property_:
                point += calc_point(property_[method])

        return point

    except LoaderFileError:
        raise


# CHECKED
# restituisce un vocabolario {nome_proprietà: [elenco_sottoproprietà]
def load_relation():
    properties = settings.load_json_read(npath + "properties_settings.json")

    linked = []
    relation = {}
    for property_ in properties:
        for each in properties[property_]:
            linked.append(each["property"])
        relation[property_] = linked
        linked = []

    return relation


# CHECKED
# restituisce l'elenco di proprietà che hanno sottoproprietà
def load_sup_link():
    mprint("LOG: loading list of properties with sub properties")
    try:
        properties = settings.load_json_read(npath + "properties_settings.json")

        linked = []
        for property_ in properties:
            if property_ != "result":
                linked.append(property_)

        return linked

    except LoaderFileError:
        raise


def load_accepted_formats():
    formats = settings.load_json_read(npath + "format.json")

    accepted_formats = []

    for format_ in formats:
        accepted_formats.append(format_)

    return accepted_formats


def load_prova():
    with open("prova2.json", "r") as f:
        payload = json.load(f)

    return payload


def load_vocabularies():
    with open("settings/settings_file/vocabularies.json", "r") as f:
        vocabularies = json.load(f)

    return vocabularies


# restituisce i formati di permalink accettati
def load_permalink():
    try:
        permalinks = settings.load_json_read(npath + "permanent_link.json")["formats"]

        return permalinks

    except LoaderFileError:
        raise


def load_allowed_formats():
    allowed_formats = settings.load_json_read(npath + "format.json")

    return allowed_formats


def get_delimiter(file):
    with open("temp/" + file, 'r') as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter


def load_csv(file):
    with open("temp/" + file, "r") as csv_f:
        df = pd.read_csv(csv_f)

    return df


def load_methods():
    return settings.load_json_read("settings/settings_file/methods.json")["methods"]


def load_update_date():
    f = settings.load_json_read(npath + "update.json")

    return f["date"]


def save_update_date():
    today = {"date" : str(datetime.datetime.now())}
    settings.write_json_read(npath + "update.json", today)
    return


class LoaderFileError(Exception):
    pass