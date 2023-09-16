import inspect
from log.error import error
report = ""


def start_report():
    global report
    report += "euFAIR - THE TOOL GOR YOUR EU ORIENTED FAIRIFICATION\n"


def add_to_report(str_):
    global report
    report += str_ + "\n"


def save_report(file: str):
    path = file.replace("\\", "/")
    try:
        with open(path, "w") as f:
            f.write(report)

    except IOError as e:
        print("ERROR: Can't open the report")
        error(e, inspect.currentframe())

        raise ReporterFileError

    except Exception as e:
        print("ERROR: Unexpected error:", e, type(e))
        error(e, inspect.currentframe())
        raise ReporterFileError


class ReporterFileError(Exception):
    pass