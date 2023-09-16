import inspect
import json

from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
from log.error import error


def check_for_new_property():
    mprint("LOG: checking for new property", bc.BLUE)
    try:
        with open("settings/settings_file/properties_settings.json", "r") as f1, \
                open("settings/settings_file/metadata_schema.json", "r") as f2:
            properties = json.load(f1)
            schema_j = json.load(f2)
            schema = json.dumps(schema_j)

            warning = []
            for key in properties.keys():
                if schema.find(key) == -1:
                    warning.append(key)
                for _property in properties[key]:
                    if schema.find(_property["property"]) == -1:
                        warning.append(_property["property"])

            if warning:
                mprint("WARNING: New property found, this properties could be not valid ->", bc.YELL)
                mprint(str(warning))
                return warning
            else:
                mprint("LOG: no new property found", bc.GREEN)

    except FileNotFoundError as e:
        mprint("ERROR: Property file not found in preloading", bc.RED, 0)
        error(e, inspect.currentframe())
        raise PreloadingFileError

    except IOError as e:
        mprint("ERROR: Can't open the settings files in preloading", bc.RED, 0)
        error(e, inspect.currentframe())

        raise PreloadingFileError

    except Exception as e:
        mprint("ERROR: Unexpected error:" + str(e) + str(type(e)), bc.RED, 0)
        error(e, inspect.currentframe())
        raise PreloadingFileError


def new_property_from_warning(warning):
    mprint("LOG: saving new properties")
    try:
        with open("settings/settings_file/metadata_schema.json", "r") as f:
            schema = json.load(f)

            for each in warning:
                schema.update({each: "string"})
                print("LOG: new property from warning: " + each + " created")

            mprint("LOG: property from warning created")

        with open("settings/settings_file/metadata_schema.json", "w") as f:
            json.dump(schema, f, indent=4, separators=(',', ': '))
            mprint("LOG: new property from warning saved")

    except FileNotFoundError as e:
        mprint("ERROR: Schema file not found in preloading", bc.RED, 0)
        error(e, inspect.currentframe())
        raise PreloadingFileError

    except IOError as e:
        mprint("ERROR: Can't open the schema file in preloading", bc.RED, 0)
        error(e, inspect.currentframe())
        raise PreloadingFileError

    except Exception as e:
        mprint("ERROR: Unexpected error:" + str(e) + str(type(e)), bc.RED, 0)
        error(e, inspect.currentframe())
        raise PreloadingFileError


class PreloadingFileError(Exception):
    pass