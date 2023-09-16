import settings


def guidelines_i(file_name):
    try:
        max_point = 0
        max_point += 1
        scored_point = 0

        delimiter = settings.get_delimiter(file_name)

        if delimiter == ";":
            scored_point += 1

    except Exception as e:
        print(e)
    return max_point, scored_point
