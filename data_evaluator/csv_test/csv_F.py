import settings
import pandas as pd


def guidelines_f(dataset_name):
    try:
        csv_f = settings.load_csv(dataset_name)
        max_point = 0
        max_point += 1

        value_count = csv_f.count().sum().sum()

        null_value_count = csv_f.isna().sum().sum()
        print("LOG: found " + str(null_value_count) + "/" + str(value_count+null_value_count) + " null value")

        scored_point = value_count / (value_count + null_value_count)
    except Exception as e:
        print(e)
    return max_point, scored_point

