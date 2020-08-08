from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .const import LAST_ACTION, LAST_DATA, CANCEL_CREATION_GROUP_CALLBACK, EMPTY_ACTION


def get_first_or_default(collection, default=None):
    if collection:
        return collection[0]
    return default


def create_button_columns(buttons, column_count=2):
    max_len = len(buttons)
    for i in range(0, max_len, column_count):
        yield buttons[i:min(i + column_count, max_len)]


def clear_last(context):
    context.user_data[LAST_ACTION] = EMPTY_ACTION
    context.user_data[LAST_DATA] = None


def set_last(context, action, data=None):
    context.user_data[LAST_ACTION] = action
    context.user_data[LAST_DATA] = data


def create_cancel_button(text):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=f'{CANCEL_CREATION_GROUP_CALLBACK}')]])
