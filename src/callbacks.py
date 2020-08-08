from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .const import LAST_ACTION, LAST_DATA, CHANGE_ACTION, MESSAGE_ACTION_CALLBACK, MESSAGE_CALLBACK, DONE, CHANGE

from .model import Note
from .process import create_button_columns


def get_note_actions(note_id):
    return InlineKeyboardMarkup(create_button_columns([
        InlineKeyboardButton('Done', callback_data=f'{MESSAGE_ACTION_CALLBACK},{DONE},{note_id}'),
        InlineKeyboardButton('Change', callback_data=f'{MESSAGE_ACTION_CALLBACK},{CHANGE},{note_id}')
    ], 1))


def message_action_callback(update, context, params):
    query = update.callback_query
    action, note_id = params
    if action == DONE:
        Note.delete_by_id(note_id)
        message = 'Deleted'
    elif action == CHANGE:
        context.user_data[LAST_ACTION] = CHANGE_ACTION
        context.user_data[LAST_DATA] = {'note_id': note_id}
        message = 'Write new note:'
    else:
        message = 'Technical error: repeat pleas'

    query.answer()
    query.edit_message_text(text=message)


def message_callback(update, context, params):
    query = update.callback_query
    note_id, = params
    note = Note.get_by_id(note_id)

    query.answer()
    query.edit_message_text(text=note.message, reply_markup=get_note_actions(note_id))


CALLBACK_MAPPING = {
    MESSAGE_CALLBACK: message_callback,
    MESSAGE_ACTION_CALLBACK: message_action_callback
}
