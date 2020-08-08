from .const import LAST_DATA, CHANGE_ACTION, NOTE_ACTION, CREATE_GROUP_ACTION
from .model import Note
from .process import create_group
from .helpers import clear_last
from .internalization import get_message


def change_action(update, context, group):
    text = update.message.text
    data = context.user_data.get(LAST_DATA)

    note = Note.get_by_id(data.get('note_id'))
    note.message = text
    note.save()

    clear_last(context)
    update.message.reply_text(get_message(update, context, 'Changes are saved'))


def note_action(update, context, group):
    data = context.user_data.get(LAST_DATA)
    Note.create(group=group.id, message=data.get('note'))

    clear_last(context)
    update.message.reply_text(get_message(update, context, 'Note is saved'))


def create_group_action(update, context, group):
    text = update.message.text
    clear_last(context)
    create_group(update, context, text)


ACTION_MAPPING = {
    CHANGE_ACTION: change_action,
    NOTE_ACTION: note_action,
    CREATE_GROUP_ACTION: create_group_action
}
