import inspect
import json
import requests
from bs4 import BeautifulSoup

from log.error import error
import settings
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc


def retrieve_payload_europa(dataset_id):
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"https://data.europa.eu/api/hub/search/datasets/{dataset_id}")
        status_code = response.status_code

        mprint("LOG: connection established -> status_code: " + str(status_code), bc.GREEN)

        match status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN, 0)
                payload = json.loads(response.text)
                return payload

            case 400:
                mprint("ERROR: Invalid request", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 404:
                mprint("ERROR: Dataset non found. ID not valid", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 500:
                mprint("ERROR: Internal server error", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case _:
                mprint("Error: Unspecified connection error " + str(response.status_code), bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


def retrieve_payload_italia(dataset_id):
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"https://www.dati.gov.it/opendata/api/3/action/package_show?id={dataset_id}")
        status_code = response.status_code

        mprint("LOG: connection established -> status_code: " + str(status_code), bc.GREEN)

        match status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN, 0)
                payload = json.loads(response.text)
                return payload

            case 400:
                mprint("ERROR: Invalid request", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 404:
                mprint("ERROR: Dataset non found. ID not valid", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 500:
                mprint("ERROR: Internal server error", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case _:
                mprint("Error: Unspecified connection error " + str(response.status_code), bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


def retrieve_payload_italia2(dataset_id):
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"https://www.dati.gov.it/base-dati/api/3/action/package_show?id={dataset_id}")
        status_code = response.status_code

        mprint("LOG: connection established -> status_code: " + str(status_code), bc.GREEN)

        match status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN)
                payload = json.loads(response.text)
                return payload

            case 400:
                mprint("ERROR: Invalid request", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 404:
                mprint("ERROR: Dataset non found. ID not valid", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 500:
                mprint("ERROR: Internal server error", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case _:
                mprint("Error: Unspecified connection error " + str(response.status_code), bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


def retrieve_payload_ckan(dataset_id, url):
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"{url}/api/3/action/package_show?id={dataset_id}")
        status_code = response.status_code

        mprint("LOG: connection established -> status_code: " + str(status_code), bc.GREEN)

        match status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN)
                payload = json.loads(response.text)
                return payload

            case 400:
                mprint("ERROR: Invalid request", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 404:
                mprint("ERROR: Dataset non found. ID not valid", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 500:
                mprint("ERROR: Internal server error", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case _:
                mprint("Error: Unspecified connection error " + str(response.status_code), bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


def retrieve_payload_generic(url):
    mprint("LOG: sending API request", bc.BLUE)

    try:

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        responses = []
        for link in soup.find_all('a'):
            if link.get('href') is not None:
                if link.get('href').split('.')[-1] == 'json' or link.get('href').split('.')[-1] == 'rdf':
                    response = requests.get(link.get('href'))
                    if response.status_code == 200:
                        responses.append(response)

        good_responses = []
        for response in responses:
            try:
                good_responses.append(response.json())
            except requests.exceptions.JSONDecodeError:
                pass

        return good_responses

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        print(e)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


def find_unique_files(payload):
    files = []
    mprint("LOG: finding file links in metadata", bc.ENDC, 0)

    for distribution in payload["result"]["resources"]:
        if "download_url" in distribution \
                and distribution["download_url"] \
                and distribution["download_url"] != []:
            mprint("LOG: found download_url", bc.ENDC, 0)
            files.append(distribution["download_url"])
        if "access_url" in distribution \
                and distribution["access_url"] \
                and distribution["access_url"] != []:
            mprint("LOG: found access url", bc.ENDC, 0)
            files.append(distribution["access_url"])
        if "url" in distribution \
                and distribution["url"] \
                and distribution["url"] != []:
            files.append(distribution["url"])

    unique_file = set()
    unique_link = set()
    for file in files:
        unique_link.add(file)
    for file in files:
        unique_file.add(file.split("/")[-1])

    return unique_link, unique_file


def find_format_for_file(file_list):
    mprint("LOG: finding best format", bc.ENDC, 0)
    allowed_formats = settings.load_accepted_formats()

    file_with_formats = {}

    for file in file_list:
        file_format = file.split(".")[-1]
        file_name = "".join([x for x in file.split(".")[:-1]])
        if file_name:
            if file_format in allowed_formats:
                if file_name in file_with_formats:
                    mprint("LOG: found accepted format for->" + file_name + " : " + file_format, bc.ENDC, 0)
                    file_with_formats[file_name].append(file_format)
                else:
                    file_with_formats[file_name] = []
                    mprint("LOG: found accepted format for->" + file_name + " : " + file_format, bc.ENDC, 0)
                    file_with_formats[file_name].append(file_format)
            else:
                mprint("LOG: file not supported ->" + file, bc.ENDC, 0)

        else:
            mprint("LOG: link not valid", bc.ENDC, 0)

    return file_with_formats


def find_best_formats(file_with_formats):
    mprint("LOG: choosing the best format from the available", bc.ENDC, 0)
    allowed_formats = settings.load_allowed_formats()
    if not file_with_formats:
        return 0

    chosen_files = []
    for file in file_with_formats:
        best_format = ""
        for file_format in file_with_formats[file]:
            if best_format:
                if allowed_formats[file_format]["id"] < allowed_formats[best_format]["id"]:
                    best_format = file_format
            else:
                best_format = file_format

        mprint("LOG: best format for '" + file + "' : " + best_format, bc.ENDC, 0)
        chosen_files.append(file + "." + best_format)

    return chosen_files


def retrieve_dataset(url) -> str:
    try:
        dataset = requests.get(url)

        if dataset.status_code not in range(200, 400):
            mprint("ERROR: connection error", bc.RED)
            return -1

        dataset_name = url.split("/")[-1]

        mprint("LOG: connection established. downloading file", bc.GREEN)
        with open("temp/" + dataset_name, "wb") as file:
            file.write(dataset.content)

        return dataset_name

    except Exception:
        raise


def retrieve_distribution_metrics(dataset_id, distribution_id):
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"https://data.europa.eu/api/mqa/cache/datasets/{dataset_id}/distributions")
        mprint("LOG: connection established", bc.GREEN)

        match response.status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN)
                payload = json.loads(response.text)
                for distribution in payload["result"]["results"]:
                    if distribution[0]["info"]["distribution-id"] == distribution_id:
                        return distribution[0]

            case 400:
                mprint("ERROR: Invalid request", bc.RED)
                return 0

            case 404:
                mprint("ERROR: Dataset non trovato. Probabile ID non valido", bc.RED)
                return 0

            case 500:
                mprint("ERROR: Internal server error", bc.RED)

    except requests.exceptions.ConnectionError:
        mprint("ERROR: Errore di connessione. Controlla la rete", bc.RED)
        return 0

    except requests.exceptions.HTTPError:
        mprint("ERROR: Invalid HTTP response")

    except requests.exceptions.Timeout:
        mprint("ERROR: Il server ha messo troppo tempo a rispondere", bc.RED)

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Errore generico: " + str(e), bc.RED)


def retrieve_dataset_list():
    mprint("LOG: sending API request", bc.BLUE)

    try:
        response = requests.get(f"https://www.dati.gov.it/opendata/api/3/action/package_list")
        status_code = response.status_code

        mprint("LOG: connection established -> status_code: " + str(status_code), bc.GREEN)

        match status_code:
            case 200:
                mprint("LOG: Valid request. Retrieving payload", bc.GREEN)
                payload = json.loads(response.text)
                return payload

            case 400:
                mprint("ERROR: Invalid request", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 404:
                mprint("ERROR: Dataset non found. ID not valid", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case 500:
                mprint("ERROR: Internal server error", bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

            case _:
                mprint("Error: Unspecified connection error " + str(response.status_code), bc.RED, 0)
                error(("status code:", status_code), inspect.currentframe())
                raise RetrieveRequestError

    except requests.exceptions.ConnectionError as e:
        mprint("ERROR: Connection error. Check connection", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.HTTPError as e:
        mprint("ERROR: Invalid HTTP response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.Timeout as e:
        mprint("ERROR: Server took too much to give response", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except requests.exceptions.RequestException as e:
        mprint("ERROR: Unspecified error in request: ", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError

    except RetrieveRequestError:
        raise

    except Exception as e:
        mprint("ERROR: Unspecified error", bc.RED, 0)
        error(e, inspect.currentframe())
        raise RetrieverConnectionError


class RetrieveRequestError(Exception):
    """Error in the request response, the metadata could not be retrieved"""

    def __init__(self):
        pass


class RetrieverConnectionError(Exception):
    """Error in the loading of the cloud service, this error compromise the comparison between old and new datasets"""

    def __init__(self):
        pass
