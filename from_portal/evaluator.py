import datetime
import inspect
import json
import re
from urllib.parse import urlparse, urlunparse


import cloud_writer.starter, cloud_writer.downloader
import data_evaluator
import metadata_evaluator
import settings
from event_bus import event_bus
from log.error import error
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
from db_manager import database
from data_retriever import retriever
from cloud_writer.file_creator import write_json_read as write_temp
from cloud_writer.file_creator import delete_file

from cloud_writer.uploader import upload

methods = ["DCAT_AP", "DCAT_AP-IT", "merged"]


def save_payload(cat, dataset_id, payload, drive_service):
    file_name = cat + '-' + dataset_id + str(datetime.datetime.now()).replace(' ', '-')
    file_name = re.sub(r'[^\w\-_.]', '-', file_name)

    write_temp(file_name, payload)
    file_id = upload(file_name, dataset_id, drive_service)

    delete_file(file_name)

    return file_id


def load_old_payload(cat, dataset_id, drive_service):
    old_id = cloud_writer.downloader.search_folder_and_get_latest_file(dataset_id, cat, drive_service)
    if old_id:
        return cloud_writer.downloader.download_file(old_id, drive_service)

    return None


def metadata_retrieving_europa(dataset_id_):
    payload_ = None
    while payload_ is None:
        try:
            payload_ = retriever.retrieve_payload_europa(dataset_id_)
            return payload_

        # payload_retrieved = settings.load_prova()
        except retriever.RetrieveRequestError as e:
            error(str(e) + ' for ' + dataset_id_, inspect.currentframe())
            return -1
        except retriever.RetrieverConnectionError as e:
            error(str(e) + ' for ' + dataset_id_, inspect.currentframe())
            return -1


def metadata_retrieving_italia(dataset_id_):
    payload_ = None

    while payload_ is None:
        try:
            payload_ = retriever.retrieve_payload_italia(dataset_id_)
            return payload_

        except:
            try:
                payload_ = retriever.retrieve_payload_italia2(dataset_id_)
                return payload_
            # payload_retrieved = settings.load_prova()
            except retriever.RetrieveRequestError:
                return -1
            except retriever.RetrieverConnectionError:
                return -1


def metadata_retrieving_ckan(dataset_ids_, url_):
    for dataset_id_ in dataset_ids_:
        try:
            payload_ = retriever.retrieve_payload_ckan(dataset_id_, url_)
            return payload_

        except retriever.RetrieveRequestError:
            print(dataset_id_ + " not valid for ckan")
        except retriever.RetrieverConnectionError:
            print(dataset_id_ + " not valid for ckan")


def metadata_retrieving_generic(payload_, url_):
    try:
        payloads_ = retriever.retrieve_payload_generic(payload_)
        for payload_generic in payloads_:
            if payload_generic.find("metadata") != -1 or payload_generic.find("result") != 1:
                return payload_generic

    except retriever.RetrieveRequestError:
        return -1
    except retriever.RetrieverConnectionError:
        return -1


def metadata_evaluating_europa(dataset_id_, method_, payload_):
    return metadata_evaluator.metadata_evaluator_europa(dataset_id_, method_, payload_)


def metadata_evaluating_italia(dataset_id_, method_, payload_, eu_dataset_id_, caller_=None):
    return metadata_evaluator.metadata_evaluator_italia(dataset_id_, method_, payload_, eu_dataset_id_, caller_)


def metadata_evaluating_generic(dataset_id_, method_, payload_, dataset_url_):
    return metadata_evaluator.metadata_evaluator_generic(dataset_id_, method_, payload_, dataset_url_)


def retrieve_file_list(payload):
    print("LOG: fining file links")
    file_list = retriever.find_unique_files(payload)[1]
    file_links = retriever.find_unique_files(payload)[0]
    unique_file_list = retriever.find_format_for_file(file_list)
    chosen_files = retriever.find_best_formats(unique_file_list)

    if not chosen_files:
        return 0
    chosen_links = []
    print(chosen_files)
    for file in chosen_files:
        for link in file_links:
            if link.find(file) != -1:
                chosen_links.append(link)
                break

    print("LOG: file link found: " + "".join([x + " / " for x in chosen_links]))

    return chosen_links


def data_retrieving(payload):
    files = set()
    files_name = set()
    allowed_formats = settings.load_allowed_formats()
    chosen_files = []

    # tutti i file disponibili
    for distribution in payload["result"]["resources"]:
        if "download_url" in distribution \
                and distribution["download_url"] \
                and distribution["download_url"] != []:
            print("LOG: found download_url")
            files.add(distribution["download_url"])
        if "access_url" in distribution \
                and distribution["access_url"] \
                and distribution["access_url"] != []:
            print("LOG: found access url")
            files.add(distribution["access_url"])
        if "url" in distribution \
                and distribution["url"] \
                and distribution["url"] != []:
            files.add(distribution["url"])
            print("LOG: found url")

    # unique file name
    for file in files:
        print('file')
        file_name = file.split("/")[-1]
        if file_name.find(".") != -1:
            file_name_no_format = file_name.split(".")[-2]
            files_name.add(file_name_no_format)

    # for every file find all its formats
    for name in files_name:
        file_with_formats = []

        for file in files:
            if file.find(name) != -1:
                file_with_formats.append(file)

        # find best format
        format_available = []
        for file in file_with_formats:
            format_ = file.split(".")[-1]
            format_available.append(format_)

        best_file = ""

        print(file_with_formats)
        for file in file_with_formats:
            if best_file != "":
                if file.split(".")[-1] in allowed_formats:
                    if allowed_formats[file.split(".")[-1]]["id"] < allowed_formats[best_file.split(".")[-1]]["id"]:
                        best_file = file
            else:
                if file.split(".")[-1] in allowed_formats:
                    best_file = file

        chosen_files.append(best_file)

    if not chosen_files:
        return None

    return chosen_files


def data_evaluating(dataset_name, payload, link, method, id_europa):
    return data_evaluator.data_evaluator(dataset_name, payload, link, method, id_europa)


def update_eval():
    dataset_ids = database.retrieve_id_to_update()

    if dataset_ids:
        event_bus.publish({'type': 'portal_start'})
        drive_service = cloud_writer.starter.start()

        for idx, dataset_id in enumerate(dataset_ids):
            eu_dataset_id = 'NULL'

            event = {
                'type': 'update_text_toplevel',
                'text': f'UPDATING DATASET {idx + 1}/{len(dataset_ids)}: {dataset_id[0]}',
                'text2': '',
                'text3': '',
                'text1': ''
            }
            event_bus.publish(event)

            if dataset_id[1] is not None:

                event = {
                    'type': 'update_text_toplevel',
                    'text1': "data.europa.eu",
                }
                event_bus.publish(event)

                # fase europa
                mprint("METADATA_EUROPA", bc.YELL)

                eu_dataset_id = dataset_id[1]
                print(dataset_id)

                mprint("METAretriever", bc.YELL)
                mprint(f"FOR {eu_dataset_id}", bc.YELL)

                payload = metadata_retrieving_europa(eu_dataset_id)
                tried = 0

                is_modified = 0

                while payload == -1 and tried < 3:
                    payload = metadata_retrieving_europa(eu_dataset_id)
                    tried += 1

                if payload == -1:
                    mprint('FAILED TO RETRIEVE EUROPA PAYLOAD', bc.RED)
                else:
                    old_id = load_old_payload('eu', dataset_id[0], drive_service)

                    file_id = save_payload('eu', dataset_id[0], payload, drive_service)

                    if old_id:
                        old_payload = settings.load_txt_to_json('temp/' + old_id + '.txt')

                        if json.dumps(old_payload) != json.dumps(payload):

                            for key in old_payload['result'].keys():
                                print(key)
                                if key != 'modified':
                                    if payload['result'][key] != old_payload['result'][key]:
                                        is_modified = 1

                        delete_file(old_id)

                    if not is_modified:
                        print('Il file non sembra modificato')

                    for method in methods:
                        event = {
                            'type': 'update_text_toplevel',
                            'text2': f"METHOD: {method}",
                        }
                        event_bus.publish(event)
                        mprint("METADATA EVALUATOR", bc.GREEN)

                        metadata_result_europa = metadata_evaluating_europa(eu_dataset_id, method, payload)

                        database.create_new_metadata_evaluation(dataset_id[0], "data.europa.eu", method,
                                                                metadata_result_europa, is_modified, file_id)

                        event = {
                            'type': 'update_text_toplevel',
                            'text3': "UPDATED",
                        }
                        event_bus.publish(event)

            else:
                event = {
                    'type': 'update_text_toplevel',
                    'text1': "NO data.europa.eu",
                }
                event_bus.publish(event)

            is_modified = 0

            mprint("METADATA ITALIA", bc.YELL)

            event = {
                'type': 'update_text_toplevel',
                'text1': "dati.gov.it",
            }
            event_bus.publish(event)

            mprint("METAretriever", bc.YELL)
            mprint(f"FOR {dataset_id[0]}", bc.YELL)

            payload_ita = metadata_retrieving_italia(dataset_id[0])

            old_id_ita = load_old_payload('it', dataset_id[0], drive_service)

            file_id = save_payload('it', dataset_id[0], payload_ita, drive_service)

            if old_id_ita:
                print(f'OLD ITA: {old_id_ita}')
                old_payload = settings.load_txt_to_json('temp/' + old_id_ita + '.txt')

                if json.dumps(old_payload) != json.dumps(payload_ita):

                    for key in old_payload['result'].keys():
                        print(key)
                        if key != 'modified':
                            if payload_ita['result'][key] != old_payload['result'][key]:
                                is_modified = 1

            if not is_modified:
                print('Il file non sembra modificato')

            for method in methods:
                event = {
                    'type': 'update_text_toplevel',
                    'text2': f"METHOD: {method}",
                }
                event_bus.publish(event)

                mprint("METADATA EVALUATOR", bc.GREEN)
                metadata_result_italia = metadata_evaluating_italia(dataset_id[0], method, payload_ita, eu_dataset_id)

                database.create_new_metadata_evaluation(dataset_id[0], "dati.gov.it", method,
                                                        metadata_result_italia, is_modified, file_id)

            is_modified = 0

            mprint("METADATA CKAN", bc.YELL)

            mprint("METAretriever", bc.YELL)
            mprint(f"FOR {dataset_id[0]}", bc.YELL)

            if "url" in payload_ita["result"] and payload_ita["result"]["url"] is not None:

                id_to_try = [dataset_id[0]]

                if payload_ita["result"]["identifier"] is not None:
                    id_to_try.append(payload_ita["result"]["identifier"])

                temp_url = urlparse(payload_ita["result"]["url"])
                url = temp_url.scheme + "://" + str(temp_url.hostname)

                event = {
                    'type': 'update_text_toplevel',
                    'text1': f"{temp_url.hostname}",
                }
                event_bus.publish(event)

                print("Trying CKAN api")
                payload_CKAN = metadata_retrieving_ckan(id_to_try, url)

                if payload_CKAN:
                    old_id = load_old_payload('ge', dataset_id[0], drive_service)

                    file_id = save_payload('ge', dataset_id[0], payload_CKAN, drive_service)

                    if old_id:
                        old_payload = settings.load_txt_to_json('temp/' + old_id + '.txt')

                        if json.dumps(old_payload) != json.dumps(payload_ita):

                            for key in old_payload['result'].keys():
                                print(key)
                                if key != 'modified':
                                    if payload_ita['result'][key] != old_payload['result'][key]:
                                        is_modified = 1

                        delete_file(old_id)

                    if not is_modified:
                        print('Il file non sembra modificato')

                    for method in methods:
                        event = {
                            'type': 'update_text_toplevel',
                            'text2': f"METHOD: {method}",
                        }
                        event_bus.publish(event)

                        mprint("METADATA EVALUATOR", bc.GREEN)
                        metadata_result_CKAN = metadata_evaluating_italia(dataset_id[0], method, payload_CKAN,
                                                                          eu_dataset_id, payload_ita)
                        database.create_new_metadata_evaluation(dataset_id[0], temp_url.hostname,
                                                                method, metadata_result_CKAN, is_modified, file_id)

                else:

                    mprint("METADATA GENERIC", bc.YELL)

                    mprint("METAretriever", bc.YELL)
                    mprint(f"FOR {dataset_id}", bc.YELL)
                    if "url" in payload_ita["result"]:

                        parsed_url = urlparse(payload_ita["result"]["url"])

                        if parsed_url.scheme == '':
                            url_to_or = urlunparse(parsed_url._replace(scheme='http'))

                        else:
                            url_to_or = urlunparse(parsed_url)

                        try:
                            payloads_generics = retriever.retrieve_payload_generic(url_to_or)

                            old_id = load_old_payload('ge', dataset_id[0], drive_service)

                            file_id = save_payload('ge', dataset_id[0], payloads_generics, drive_service)

                            if old_id:
                                old_payload = settings.load_txt_to_json('temp/' + old_id + '.txt')

                                if json.dumps(old_payload) != json.dumps(payload_ita):
                                                is_modified = 1

                                delete_file(old_id)

                            if not is_modified:
                                print('Il file non sembra modificato')

                            for method in methods:
                                event = {
                                    'type': 'update_text_toplevel',
                                    'text2': f"METHOD: {method}",
                                }
                                event_bus.publish(event)
                                mprint("METADATA EVALUATOR", bc.GREEN)
                                metadata_result_generic = metadata_evaluating_generic(dataset_id[0], method,
                                                                                      payloads_generics, url_to_or)
                                database.create_new_metadata_evaluation(dataset_id[0], temp_url.hostname,
                                                                        method, metadata_result_generic, is_modified,
                                                                        file_id)
                        except:
                            pass

            datasets_link = data_retrieving(payload_ita)
            print("sei qui ", datasets_link)
            if datasets_link != [''] and datasets_link is not None:
                for dataset_link in datasets_link:
                    if dataset_link != '':
                        dataset_name = retriever.retrieve_dataset(dataset_link)

                        print(''.join(dataset_name.split(".")[:-1]))

                        file_id = cloud_writer.uploader.upload(''.join(dataset_name.split(".")[:-1]), dataset_id[0],
                                                               drive_service, dataset_name.split(".")[-1])
                        print(dataset_name, dataset_link)

                        mprint("WORKING ON " + dataset_link, bc.CYAN)

                        print(dataset_name, dataset_link)

                        is_modified = 0

                        this_distribution = ''
                        for distribution in payload_ita["result"]["resources"]:

                            if "download_url" in distribution \
                                    and distribution["download_url"] \
                                    and distribution["download_url"] != [] \
                                    and distribution["download_url"] == dataset_link:
                                this_distribution = distribution
                            elif "access_url" in distribution \
                                    and distribution["access_url"] \
                                    and distribution["access_url"] != [] \
                                    and distribution["access_url"] == dataset_link:
                                this_distribution = distribution
                            elif "url" in distribution \
                                    and distribution["url"] \
                                    and distribution["url"] != [] \
                                    and distribution["url"] == dataset_link:
                                this_distribution = distribution

                        this_old_distribution = ''
                        if old_id_ita:
                            old_payload = settings.load_txt_to_json('temp/' + old_id_ita + '.txt')

                            for distribution in old_payload["result"]["resources"]:
                                if "download_url" in distribution \
                                        and distribution["download_url"] \
                                        and distribution["download_url"] != [] \
                                        and distribution["download_url"] == dataset_link:
                                    this_old_distribution = distribution
                                elif "access_url" in distribution \
                                        and distribution["access_url"] \
                                        and distribution["access_url"] != [] \
                                        and distribution["access_url"] == dataset_link:
                                    this_old_distribution = distribution
                                elif "url" in distribution \
                                        and distribution["url"] \
                                        and distribution["url"] != [] \
                                        and distribution["url"] == dataset_link:
                                    this_old_distribution = distribution

                            if json.dumps(this_old_distribution) != json.dumps(this_distribution):

                                for key in this_old_distribution.keys():
                                    print(this_old_distribution.keys())
                                    print(key)
                                    if key != 'last_modified':
                                        print(this_distribution)
                                        if this_distribution[key] != this_old_distribution[key]:
                                            is_modified = 1

                        for method in methods:
                            data_result = data_evaluating(dataset_name, payload_ita, dataset_link, method, eu_dataset_id)

                            database.create_new_data_evaluation(dataset_id[0], file_id, dataset_name, method,
                                                                data_result, is_modified)

                        delete_file(''.join(dataset_name.split(".")[:-1]), dataset_name.split(".")[-1])
                if old_id_ita:
                    delete_file(old_id_ita)
                database.set_update_date(dataset_id[0])

    else:
        event_bus.publish({'type': 'update_done_toplevel'})