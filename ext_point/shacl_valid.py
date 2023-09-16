import json

import requests


def get_validation(report):
    response = requests.post("https://data.europa.eu/api/mqa/shacl/validation/report", report)

    if response.status_code == 200:
        print(response)
        print(json.dumps(response.json(), indent= 4))

    else: print(response.status_code)