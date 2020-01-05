from telegram.ext import Updater 

# Read XML
from xml.dom import minidom

# To monotor
import logging

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_token():
    # parse an xml file by name
    mydoc = minidom.parse('credentials.xml')

    tokens = mydoc.getElementsByTagName('token')

    token = 'TOKEN'
    if not tokens:
        raise Exception("Provide a token")
    else:
        token = tokens[0].firstChild.data

    return token


# Call the function everytime the start comman is called
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# Echo every text message
def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def alarm(context):
    # Send the alarm message
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

def main():
    # Read the token
    token = get_token()

    # Create Updater & Dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # All handlers of the bot
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    echo_handler = MessageHandler(Filters.text, echo)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(inline_caps_handler)
    dispatcher.add_handler(unknown_handler, group=1) # Trigers the last one

    # Log all errors 
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Stop the bot gracefully
    updater.idle()

if __name__ == "__main__":
    main()
