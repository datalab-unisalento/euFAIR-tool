import inspect

import requests
import json
from utility.utility import myprint as mprint
from log.error import error

def retrieve_mqa_point(dataset_id):
    try:
        response = requests.get(f"https://data.europa.eu/api/mqa/cache/datasets/{dataset_id}")

        if response.status_code == 200:
            payload = json.loads(response.text)

            return payload["result"]["results"][0]["info"]["score"]
        else:
            return 0

    except requests.exceptions as e:
        mprint("ERROR: error in mqa retrival")
        error(e, inspect.currentframe())
        return 0
