import json
import re
import pandas as pd


def date_time_format(df: pd.DataFrame):
    iso_format = re.compile(r"([0-3][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9](?:[+-][0-1]["
                            r"0-9](?::[0-9]{2})?|Z)?)")

    time_format = re.compile(r"(?:^|\s)((?:[0-1][0-9]|2[1-3]):[0-5][0-9]:[0-5][0-9])(?:$|\s)", re.IGNORECASE)
    date_format = re.compile(r"(?:^|\s)([0-2][0-9]{3}-[01][0-9]-[0-3][0-9])(?:$|\s)", re.IGNORECASE)

    err_time_format = re.compile(r'(?:^|\s)([0-5]?[0-9]:[0-5][0-9])(?:$|\s)')
    err_date_format = re.compile(r"(?:^|\s)((?:[0-3][0-9])?[0-9]{2}[./][01]?[0-9][./][0-3]?[0-9]|"
                                 r"[0-9]{2}[-./][01]?[0-9][-./][0-3]?[0-9]|"
                                 r"[0-3]?[0-9][-./][0-1]?[0-9][-./](?:[0-3]?[0-9])?[0-9]{2})(?:$|\s)",
                                 re.IGNORECASE)

    correct = 0
    wrong = 0

    for rowIdx, row in df.iterrows():
        for colIdx, cell in row.items():
            str_cell = str(cell)
            print(str_cell)
            iso_dates = re.findall(iso_format, str_cell)

            correct_dates = re.findall(date_format, str_cell)

            correct_times = re.findall(time_format, str_cell)

            wrong_dates = re.findall(err_date_format, str_cell)

            wrong_times = re.findall(err_time_format, str_cell)

            print(iso_dates, correct_dates, correct_times, wrong_dates, wrong_times)

            correct += len(iso_dates) + len(correct_dates) + len(correct_times)
            wrong += len(wrong_times) + len(wrong_dates)

    print(correct)
    print(wrong)
    return correct, wrong
