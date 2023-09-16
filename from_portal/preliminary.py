import inspect
import json
import requests as requests

import settings
from event_bus import event_bus
from log.error import error
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
from db_manager import database
from utility.message_box import box


def search_for_update():
    mprint('STARTING PRELIMINARY CHECK', bc.GREEN)
    mprint('CHECKING FOR NEW DATASET')
    event = {
        'type': 'update_text_toplevel',
        'text': 'SEARCHING FOR NEW DATASET',
        'text1': '',
        'text2': '',
        'text3': ''
    }
    event_bus.publish(event)
    dataset_to_add = {'opendata': [], 'basidati': []}
    dataset_old_op_id = set(database.retrieve_all_id('opendata'))
    dataset_old_bd_id = set(database.retrieve_all_id('basidati'))
    dataset_old_op_nm = set(database.retrieve_all_name('opendata'))
    dataset_old_bd_nm = set(database.retrieve_all_name('basidati'))

    try:
        event = {
            'type': 'update_text_toplevel',
            'text': 'SEARCHING FOR NEW DATASET',
            'text1': 'searching in OPENDATA',
            'text2': '',
            'text3': ''
        }
        event_bus.publish(event)
        response = requests.get("https://www.dati.gov.it/opendata/api/3/action/package_list")
        if response.status_code == 200:
            dataset_new = set(json.loads(response.text)['result'])
            missing = list(dataset_new - dataset_old_op_nm - dataset_old_op_id)

            if missing:
                dataset_to_add['opendata'] = missing


        else:
            event = {
                'type': 'update_text_toplevel',
                'text': 'SEARCHING FOR NEW DATASET',
                'text1': 'searching in OPENDATA',
                'text2': 'ERROR WITH SERVER',
                'text3': ''
            }
            event_bus.publish(event)
            error('ERROR WITH REQUEST - STATUS CODE: ' + str(response.status_code), inspect.currentframe())

        event = {
            'type': 'update_text_toplevel',
            'text': 'SEARCHING FOR NEW DATASET',
            'text1': 'searching in BASIDATI',
            'text2': '',
            'text3': ''
        }
        event_bus.publish(event)

        response = requests.get("https://www.dati.gov.it/base-dati/api/3/action/package_list")

        if response.status_code == 200:
            dataset_new = set(json.loads(response.text)['result'])

            missing = list(dataset_new - dataset_old_bd_id - dataset_old_bd_nm)

            if missing:
                dataset_to_add['basidati'] = missing


        else:
            event = {
                'type': 'update_text_toplevel',
                'text': 'SEARCHING FOR NEW DATASET',
                'text1': 'searching in BASIDATI',
                'text2': 'ERROR WITH SERVER',
                'text3': ''
            }
            event_bus.publish(event)
            error('ERROR WITH REQUEST - STATUS CODE: ' + str(response.status_code), inspect.currentframe())

        if dataset_to_add['opendata'] or dataset_to_add['basidati']:
            mprint(str(len(dataset_to_add['opendata']) + len(dataset_to_add['basidati'])) + ' NEW DATABASE FOUND',
                   bc.BLUE)
            add_new_dataset(dataset_to_add)

    except requests.RequestException as e:
        mprint('CONNECTION ERROR - NON FATAL', bc.RED)
        error(e, inspect.currentframe())


def add_new_dataset(dataset_to_add):
    err = []
    for dataset in dataset_to_add['opendata']:
        event = {
            'type': 'update_text_toplevel',
            'text': 'SEARCHING FOR NEW DATASET',
            'text1': 'ADDING TO DATABASE',
        }
        event_bus.publish(event)
        mprint('ADDING DATASET OP: ' + dataset, bc.BLUE)

        try:
            event = {
                'type': 'update_text_toplevel',
                'text1': f'ADDING {dataset} TO DATABASE',
                'text2': ''
            }
            event_bus.publish(event)
            response = requests.get(f'https://www.dati.gov.it/opendata/api/3/action/package_show?id={dataset}')

            if response.status_code == 200:
                dataset_in = json.loads(response.text)['result']

                database.add_new_database(dataset_in, 'opendata')
                mprint(dataset + ' DONE', bc.GREEN)
                event = {
                    'type': 'update_text_toplevel',
                    'text2': 'ok'
                }
                event_bus.publish(event)

            else:
                event = {
                    'type': 'update_text_toplevel',
                    'text2': 'ERROR'
                }
                event_bus.publish(event)
                mprint("CAN'T ADD " + dataset + ' connection error', bc.RED)
                err += dataset

        except requests.RequestException as e:
            event = {
                'type': 'update_text_toplevel',
                'text2': 'ERROR'
            }
            event_bus.publish(event)
            mprint("CAN'T ADD " + dataset + ' connection error', bc.RED)

            error(e, inspect.currentframe())
            err += dataset
        except database.IntegrityError:
            err += (dataset + 'require manual check, probable interception')
            event = {
                'type': 'update_text_toplevel',
                'text2': 'ERROR'
            }
            mprint("CAN'T ADD " + dataset + ' require manual check, probable interception', bc.RED)

            event_bus.publish(event)

    for dataset in dataset_to_add['basidati']:
        mprint('ADDING DATASET BD: ' + dataset, bc.BLUE)
        try:
            event = {
                'type': 'update_text_toplevel',
                'text1': f'ADDING {dataset} TO DATABASE',
            }
            event_bus.publish(event)
            response = requests.get(f'https://www.dati.gov.it/base-dati/api/3/action/package_show?id={dataset}')

            if response.status_code == 200:
                dataset_in = json.loads(response.text)['result']

                database.add_new_database(dataset_in, 'basidati')
                mprint(dataset + ' DONE', bc.GREEN)
                event = {
                    'type': 'update_text_toplevel',
                    'text2': 'ok'
                }
                event_bus.publish(event)

            else:
                event = {
                    'type': 'update_text_toplevel',
                    'text2': 'ERROR'
                }
                event_bus.publish(event)
                mprint("CAN'T ADD " + dataset + ' connection error', bc.RED)
                err += dataset

            error("CAN'T ADD NEW DATABASE: " + str(err), inspect.currentframe())

        except requests.RequestException as e:
            error(e, inspect.currentframe())
            err += dataset
            event = {
                'type': 'update_text_toplevel',
                'text2': 'ERROR'
            }
            event_bus.publish(event)
            mprint("CAN'T ADD " + dataset + ' connection error', bc.RED)

        except database.IntegrityError:
            err += dataset
            event = {
                'type': 'update_text_toplevel',
                'text2': 'ERROR'
            }
            event_bus.publish(event)
            mprint("CAN'T ADD " + dataset + ' require manual check, probable interception', bc.RED)

    if err:
        mprint('FOUND ERRORS IN NEW DATASET PLEASE CHECK LOG', bc.RED, 0)


def property_check():
    try:
        event_bus.publish({'type': 'property_check'})
        warning = settings.check_for_new_property()

        if warning:
            if box("ATTENZIONE", "Alcune proprietà potrebbero essere errate. Vuoi continuare?"):
                mprint("LOG: Asked user if continue. Said yes", bc.GREEN)
                if box("ATTENZIONE", "Vuoi salvare queste proprietà? (vedi log)"):
                    mprint("LOG: Asked user if save new property. Said yes", bc.GREEN)
                    settings.new_property_from_warning(warning)
                else:
                    mprint("LOG: new property not saved", bc.YELL)
                    return 1
                return 2
            return -1

        else:
            return 3

    except settings.preload.PreloadingFileError:
        if box("ERROR", "Errore non fatale. Vuoi saltare il preload e continuare?"):
            return 4
        return -2





