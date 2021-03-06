import logging

from config import BOT_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from .const import LAST_ACTION, CREATE_GROUP_ACTION, CANCEL_BUTTON, CLEAR_GROUP_ACTION
from .actions import ACTION_MAPPING
from .callbacks import CALLBACK_MAPPING

from .model import Group
from .helpers import get_first_or_default
from .process import create_group, get_note_from_group, process_new_note, set_last, build_menu
from .helpers import create_cancel_button, clear_last
from .internalization import get_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text(get_message(update, context, 'Start message'))


def help_command(update, context):
    update.message.reply_text(get_message(update, context, 'Help message'))


def add_group_command(update, context):
    args = context.args
    if not args:
        set_last(context, CREATE_GROUP_ACTION)
        update.message.reply_text(get_message(update, context, 'Write category name:'),
                                  reply_markup=create_cancel_button(get_message(update, context, 'Cancel addition')))
    else:
        name = ' '.join(args)
        create_group(update, context, name)


def clear_group_command(update, context):
    set_last(context, CLEAR_GROUP_ACTION)
    update.message.reply_text(get_message(update, context, 'Write the category name you want to clear'),
                              reply_markup=build_menu(update, context, True))


def on_message(update, context):
    text = update.message.text
    group = get_first_or_default(Group.get_by_user_and_name(update.effective_user.id, text))

    action = ACTION_MAPPING.get(context.user_data.get(LAST_ACTION))
    if action and text == get_message(update, context, CANCEL_BUTTON):
        clear_last(context)
        update.message.reply_text(get_message(update, context, 'Action canceled'),
                                  reply_markup=build_menu(update, context))
    elif action:
        action(update, context, group)
    elif group:
        get_note_from_group(update, context, group)
    else:
        process_new_note(update, context)


def callback_on_choose(update, context):
    query = update.callback_query
    data = query.data.split(',')
    callback = CALLBACK_MAPPING.get(data[0])
    if callback:
        callback(update, context, data[1:])
    else:
        unknown_callback(update, context, data)


def unknown_callback(update, context, params):
    logger.error(f'Unknown callback with params: {params}')
    update.message.reply_text(get_message(update, context, 'Technical error: repeat pleas'))


def start_bot():
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('add', add_group_command))
    dp.add_handler(CommandHandler('clear', clear_group_command))

    dp.add_handler(MessageHandler(~Filters.command, on_message))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_on_choose))

    updater.start_polling()
    updater.idle()
