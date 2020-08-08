from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .const import NOTE_ACTION, MESSAGE_CALLBACK, CANCEL_BUTTON

from .helpers import create_button_columns, set_last
from .model import Note, Group
from .internalization import get_message

DEFAULT_GROUPS = ['favourites', 'todo', 'watch later']


def create_group(update, context, name):
    Group.create(user_id=update.effective_user.id, name=name)
    reply_markup = build_menu(update, context)
    update.message.reply_text(get_message(update, context, 'Group is created'), reply_markup=reply_markup)


def get_note_from_group(update, context, group):
    messages = []
    for note in Note.get_by_group(group.id):
        messages.append(InlineKeyboardButton(note.message, callback_data=f'{MESSAGE_CALLBACK},{note.id}'))
    if not messages:
        update.message.reply_text(get_message(update, context, 'Category is empty'))
    else:
        update.message.reply_text(get_message(update, context, 'Select message:'),
                                  reply_markup=InlineKeyboardMarkup(create_button_columns(messages, 1)))


def process_new_note(update, context):
    text = update.message.text
    set_last(context, NOTE_ACTION, {'note': text})
    reply_markup = build_menu(update, context, cancel_button=True)
    update.message.reply_text(get_message(update, context, 'Choose group to save'), reply_markup=reply_markup)


def build_menu(update, context, cancel_button=False):
    groups = [group.name for group in get_groups_or_create_default(update, context, update.effective_user.id)]
    groups = list(create_button_columns(groups))
    if cancel_button:
        groups.append([get_message(update, context, CANCEL_BUTTON)])
    return ReplyKeyboardMarkup(groups, resize_keyboard=True)


def get_groups_or_create_default(update, context, user_id):
    groups = Group.get_by_user_id(user_id)
    if groups:
        return groups
    default = [get_message(update, context, group) for group in DEFAULT_GROUPS]
    return Group.create_groups(user_id, default)
