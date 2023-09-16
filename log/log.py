import datetime


def log(to_log):
    try:
        with open("log/log.txt", "a+") as file:
            file.writelines(["--------------------------------------------------------------------------------------\n",
                             str(datetime.datetime.now().time()), "--> ", str(to_log), "\n"])
    except Exception as e:
        print("ERROR: FATAL ERROR FOR LOG", e)


def clean_stack():
    try:
        with open("log/log.txt", "w") as file:
            pass

    except Exception as e:
        print("ERROR: FATAL ERROR FOR LOG", e)