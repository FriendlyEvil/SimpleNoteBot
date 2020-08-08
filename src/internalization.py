from .helpers import get_lang

LOCALES = {'ru', 'en'}
DEFAULT_LOCALE = 'en'

internalization = {
    "ru": {
        'Start message': 'Привет! Это бот для хранения заметок. Отправь мне сообщения, а сохраню его. \n'
                         'Напиши /help чтобы узнать мои команды',
        'Help message': '/add - добавить новую категорию',
        'Write category name:': 'Напишите имя новой категории',
        'Cancel addition': 'Отменить добавление',
        'Action canceled': 'Действие отменено',
        'Technical error: repeat pleas': 'Произошла ошибка: попробуйте снова',
        'Changes are saved': 'Изменения сохранены',
        'Note is saved': 'Заметка сохранена',
        'Done': 'Выполнено',
        'Change': 'Изменить',
        'Deleted': 'Заметка удалена',
        'Write new note:': 'Напишите новый текст:',
        'Cancel updating': 'Отменить изменение',
        'Canceled': 'Отменено',
        'Group is created': 'Новая группа успешно создана',
        'Select message:': 'Выберите заметку для просмотра:',
        'Choose group to save': 'В какую категорию добавить?',
        'Cancel': 'Отменить'
    },
    "en": {
        'Start message': 'Hi! I\'m bot for storing notes. Send me messages and I\'ll save it',
        'Help message': '/add - add a new category',
        'Write category name:': 'Write the name of the new category',
        'Cancel addition': 'Cancel addition',
        'Action canceled': 'Action canceled',
        'Technical error: repeat pleas': 'An error occurred: please try again',
        'Changes are saved': 'Changes are saved',
        'Note is saved': 'Note is saved',
        'Done': 'Done',
        'Change': 'Change',
        'Deleted': 'Note deleted',
        'Write new note:': 'Write a new text:',
        'Cancel updating': 'Undo the changes',
        'Canceled': 'Cancelled',
        'Group is created': 'The new group was created successfully',
        'Select message:': 'Select a note to view:',
        'Choose group to save': 'Choose group to save',
        'Cancel': 'Cancel'
    }
}


def _get_translate(message_key, locale):
    return internalization.get(locale, {}).get(message_key)


def _get_default(message_key):
    return _get_translate(message_key, DEFAULT_LOCALE) or message_key


def _get_message(message_key, locale):
    return _get_translate(message_key, locale) or _get_default(message_key)


def get_message(update, context, message_key):
    return _get_message(message_key, get_lang(update, context))
