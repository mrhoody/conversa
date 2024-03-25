"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define conversation states
LANGUAGE, CEFR_LEVEL, TEXT = range(3)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"""Hi {user.mention_html()}, I'm Conversa & I'm here to help you with your language learning! 
        Please choose the language you want to practice writing in today.""",
        reply_markup=ReplyKeyboardMarkup(
            [["Spanish", "French"]], one_time_keyboard=True
        ),
    )
    return CEFR_LEVEL


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        """
        Use the following commands to interact with me:\n
        /start - Start the bot\n
        /write - Get a writing prompt for Spanish or French at a desired CEFR level and get feedback on your text\n
        """
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(
    #     "I'm sorry, I don't understand that command. Please use /help to see the list of commands."
    # )
    await update.reply_mark


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give more information about Conversa to users."""
    await update.message.reply_text(
        """
        Conversa is your friendly language teacher! 
        It'll give you a hand with your writing and give you feedback on your text.
        Developed by Hud Syafiq Herman and powered by LLMs 😁
        """
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("revoked token").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
