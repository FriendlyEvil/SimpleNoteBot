from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .const import LAST_ACTION, LAST_DATA, NOTE_ACTION, MESSAGE_CALLBACK, EMPTY_ACTION

from .model import Note, Group, get_groups_or_create_default
from .helpers import create_button_columns


def clear_last(context):
    context.user_data[LAST_ACTION] = EMPTY_ACTION
    context.user_data[LAST_DATA] = None


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
    context.user_data[LAST_DATA] = {'note': text, 'message_id': 15}
    context.user_data[LAST_ACTION] = NOTE_ACTION
    save_note_to_group(update, context)


def save_note_to_group(update, context):
    reply_markup = build_menu(update, context)
    update.message.reply_text('Choose group to save', reply_markup=reply_markup)


def build_menu(update, context):
    groups = get_groups_or_create_default(update.effective_user.id)
    groups = [group.name for group in groups]
    groups = create_button_columns(groups)
    return ReplyKeyboardMarkup(groups, resize_keyboard=True)
