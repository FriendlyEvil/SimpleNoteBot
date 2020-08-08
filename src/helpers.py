def get_first_or_default(collection, default=None):
    if collection:
        return collection[0]
    return default


def create_button_columns(buttons, column_count=2):
    max_len = len(buttons)
    for i in range(0, max_len, column_count):
        yield buttons[i:min(i + column_count, max_len)]
