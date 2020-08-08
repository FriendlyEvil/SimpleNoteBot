from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .const import CHANGE_ACTION, MESSAGE_ACTION_CALLBACK, CANCEL_CREATION_GROUP_CALLBACK, \
    MESSAGE_CALLBACK, DONE, CHANGE

from .model import Note
from .process import create_button_columns, set_last
from .helpers import clear_last, create_cancel_button


def get_note_actions(note_id):
    return InlineKeyboardMarkup(create_button_columns([
        InlineKeyboardButton('Done', callback_data=f'{MESSAGE_ACTION_CALLBACK},{DONE},{note_id}'),
        InlineKeyboardButton('Change', callback_data=f'{MESSAGE_ACTION_CALLBACK},{CHANGE},{note_id}')
    ], 1))


def message_action_callback(update, context, params):
    query = update.callback_query
    action, note_id = params
    query.answer()
    if action == DONE:
        Note.delete_by_id(note_id)
        query.edit_message_text(text='Deleted')
    elif action == CHANGE:
        set_last(context, CHANGE_ACTION, {'note_id': note_id})
        query.edit_message_text(text='Write new note:', reply_markup=create_cancel_button('Cancel updating'))
    else:
        query.edit_message_text(text='Technical error: repeat pleas')


def message_callback(update, context, params):
    query = update.callback_query
    note_id, = params
    note = Note.get_by_id(note_id)

    query.answer()
    query.edit_message_text(text=note.message, reply_markup=get_note_actions(note_id))


def cancel_creation_group_callback(update, context, params):
    clear_last(context)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Canceled')


CALLBACK_MAPPING = {
    MESSAGE_CALLBACK: message_callback,
    MESSAGE_ACTION_CALLBACK: message_action_callback,
    CANCEL_CREATION_GROUP_CALLBACK: cancel_creation_group_callback
}
