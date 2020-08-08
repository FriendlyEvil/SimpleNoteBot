from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .const import LAST_ACTION, LAST_DATA, NOTE_ACTION, MESSAGE_CALLBACK, \
    CANCEL_CREATION_GROUP_CALLBACK, EMPTY_ACTION, CANCEL_BUTTON

from .model import Note, Group, get_groups_or_create_default
from .helpers import create_button_columns


def clear_last(context):
    context.user_data[LAST_ACTION] = EMPTY_ACTION
    context.user_data[LAST_DATA] = None


def set_last(context, action, data=None):
    context.user_data[LAST_ACTION] = action
    context.user_data[LAST_DATA] = data


def create_group(update, context, name):
    Group.create(user_id=update.effective_user.id, name=name)
    reply_markup = build_menu(update, context)
    update.message.reply_text('Group is created', reply_markup=reply_markup)


def get_note_from_group(update, context, group):
    messages = []
    for note in Note.get_by_group(group.id):
        messages.append(InlineKeyboardButton(note.message, callback_data=f'{MESSAGE_CALLBACK},{note.id}'))
    update.message.reply_text('Select message:', reply_markup=InlineKeyboardMarkup(create_button_columns(messages, 1)))


def process_new_note(update, context):
    text = update.message.text
    set_last(context, NOTE_ACTION, {'note': text})
    reply_markup = build_menu(update, context, cancel_button=True)
    update.message.reply_text('Choose group to save', reply_markup=reply_markup)


def create_cancel_button(text):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=f'{CANCEL_CREATION_GROUP_CALLBACK}')]])


def build_menu(update, context, cancel_button=False):
    groups = [group.name for group in get_groups_or_create_default(update.effective_user.id)]
    groups = list(create_button_columns(groups))
    if cancel_button:
        groups.append([CANCEL_BUTTON])
    return ReplyKeyboardMarkup(groups, resize_keyboard=True)
