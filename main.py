import datetime
import inspect
import threading
import time

import requests

import from_portal.preliminary, from_portal.evaluator
import settings.preload
from event_bus import event_bus
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
import gui


def do_work():
    try:
        # try:
        #     from_portal.preliminary.search_for_update()
        # except requests.RequestException:
        #     pass
        try:
            from_portal.preliminary.property_check()
        except settings.preload.PreloadingFileError:
            pass

        try:
            from_portal.evaluator.update_eval()
        except Exception as e:
            mprint(str(e), bc.RED)

        event = {'type': 'update_done_toplevel'}

        event_bus.publish(event)

    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    session_id = str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(':', '')[:-7]

    mprint('---------------------!--')
    mprint('WELCOME TO euFAIR', bc.CYAN, 0)
    mprint('SESSION ID: ' + session_id, bc.CYAN)

    app = gui.TkinterApp()

    gui.DatabaseUpdatePageOver()

    worker_thread = threading.Thread(target=do_work)
    worker_thread.start()

    app.mainloop()





