from .const import LAST_DATA, CHANGE_ACTION, NOTE_ACTION, CREATE_GROUP_ACTION, CLEAR_GROUP_ACTION
from .model import Note
from .process import create_group, build_menu
from .helpers import clear_last
from .internalization import get_message


def change_action(update, context, group):
    text = update.message.text
    data = context.user_data.get(LAST_DATA)

    note = Note.get_by_id(data.get('note_id'))
    note.message = text
    note.save()

    clear_last(context)
    update.message.reply_text(get_message(update, context, 'Changes are saved'),
                              reply_markup=build_menu(update, context))


def note_action(update, context, group):
    if check_group_not_null(update, context, group):
        data = context.user_data.get(LAST_DATA)
        Note.create(group=group.id, message=data.get('note'))
        update.message.reply_text(get_message(update, context, 'Note is saved'),
                                  reply_markup=build_menu(update, context))
    clear_last(context)


def create_group_action(update, context, group):
    text = update.message.text
    clear_last(context)
    create_group(update, context, text)


def check_group_not_null(update, context, group):
    if not group:
        update.message.reply_text('Unknown category', reply_markup=build_menu(update, context))
        return False
    return True


def clear_group_action(update, context, group):
    clear_last(context)
    if check_group_not_null(update, context, group):
        Note.delete_group(group.id)
        update.message.reply_text('Category cleared', reply_markup=build_menu(update, context))


ACTION_MAPPING = {
    CHANGE_ACTION: change_action,
    NOTE_ACTION: note_action,
    CREATE_GROUP_ACTION: create_group_action,
    CLEAR_GROUP_ACTION: clear_group_action
}
