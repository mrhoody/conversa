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

from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
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
START, CEFR_LEVEL, TEXT = range(3)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("Spanish", callback_data=1),
            InlineKeyboardButton("French", callback_data=2),
        ],
    ]

    await update.message.reply_text(
        f"""Hi {user.first_name}, I'm Conversa & I'm here to help you with your language learning! 
        Please choose the language you want to practice writing in today.""",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CEFR_LEVEL


async def select_CEFR(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Select the CEFR level for the writing prompt and grading."""

    keyboard = [
        [
            InlineKeyboardButton("A1", callback_data="A1"),
            InlineKeyboardButton("A2", callback_data="A2"),
            InlineKeyboardButton("B1", callback_data="B1"),
            InlineKeyboardButton("B2", callback_data="B2"),
            InlineKeyboardButton("C1", callback_data="C1"),
            InlineKeyboardButton("C2", callback_data="C2"),
        ],
    ]

    await update.message.reply_text(
        f"Great! Now, please select the CEFR level you want to practice writing at.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ConversationHandler.END


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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Used when there is an error in the conversation. Cancel and stop the conversation."""
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("token here").build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [],
            CEFR_LEVEL: [MessageHandler(filters.ALL, select_CEFR)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # on miscellaneous commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
