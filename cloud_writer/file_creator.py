import inspect
import json
import os

from log.error import error


def write_json_read(file_name, to_write):
    try:
        with open('temp/' + file_name + '.txt', "x") as file:
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


def delete_file(file_name, type = 'txt'):
    try:
        os.remove('temp/' + file_name  + '.' + type)
        print(f"Il file {'temp/' + file_name  + '.' + type} è stato eliminato con successo.")
    except OSError as e:
        print(f"Si è verificato un errore durante l'eliminazione del file {'temp/' + file_name  + '.' + type}: {e}")


class LoaderFileError:
    pass
