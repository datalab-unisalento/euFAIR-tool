import os
import shutil

import data_evaluator.csv_test.csv_F


def try_file(path):
    path = path.replace('\\', '/')
    print(path)
    print(os.path.isfile(path))
    print(os.path.splitext(path)[1].lower() == '.csv')
    if not os.path.isfile(path) or not os.path.splitext(path)[1].lower() == '.csv':
        print('no')
        return 0

    try:

        shutil.copy(path, 'temp/' + os.path.basename(path))
        csv_f = data_evaluator.csv_test.csv_F.guidelines_f(os.path.basename(path))
        csv_i = data_evaluator.csv_test.csv_I.guidelines_i(os.path.basename(path))
        results = {'F': {'F1': 0,
                         'F2': 0,
                         'F3': 0,
                         'F4': 0,
                         'G_F': csv_f[1]/csv_f[0]*100},
                   'A': {'A1': 0,
                         'A1.1': 0,
                         'A1.2': 0,
                         'G_A': 0},
                   'I': {'I1': 0,
                         'I2': 0,
                         'I3': 0,
                         'G_I': csv_i[1]/csv_i[0]*100},
                   'R': {'R1': 0,
                         'R1.1': 0,
                         'R1.2': 0,
                         'R1.3': 0,
                         'G_R': 0,
                         }}

        os.remove('temp/' + os.path.basename(path))

        return results
    except Exception as e:
        print(e)
        return 0