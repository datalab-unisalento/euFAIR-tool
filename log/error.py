import datetime
import inspect
from types import FrameType


def error(error, frame: FrameType):
    try:
        with open("log/log_error.txt", "a+") as file:
            file.writelines(["--------------------------------------------------------------------------------------\n",
                             str(datetime.datetime.now()), "\n",
                             str(error), "\n",
                             "caller: ", frame.f_back.f_code.co_name, " in ", inspect.getfile(frame.f_back), "\n",
                             "method called: ", frame.f_code.co_name, "\n",
                             "in: ", inspect.getfile(frame), "\n"])

    except Exception as e:
        print("ERROR: FATAL ERROR FOR STACK UP LOG", e)


def clean_stack():
    try:
        with open("log/log_error.txt", "w") as file:
            pass

    except Exception as e:
        print("ERROR: FATAL ERROR FOR STACK UP LOG", e)