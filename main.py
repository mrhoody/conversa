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

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
SELECT_LANGUAGE, SELECT_CEFR_LEVEL, INPUT_USER_TEXT, GRADE_INPUT_TEXT = range(4)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate the main conversation flow when the command /start is issued."""
    await update.message.reply_text(
        f"""Hi {update.effective_user.first_name}, I'm Conversá & I'm here to help you with your language learning!"""
    )

    await update.message.reply_text(
        f"""Please choose the language you want to practice writing in.""",
        reply_markup=ReplyKeyboardMarkup(
            [["Spanish", "French"]],
            one_time_keyboard=True,
            input_field_placeholder="Pick your language.",
        ),
    )
    return SELECT_LANGUAGE


async def select_CEFR_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.chat_data["language"] = update.message.text
    await update.message.reply_text(
        f"""You've picked {context.chat_data["language"]}. Please choose the CEFR level you want to be assessed at.""",
        reply_markup=ReplyKeyboardMarkup(
            [["A1", "A2", "B1"], ["B2", "C1", "C2"]],
            one_time_keyboard=True,
            input_field_placeholder="Pick a CEFR level.",
        ),
    )
    return SELECT_CEFR_LEVEL


async def issue_writing_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.chat_data["CEFR"] = update.message.text
    # TODO: Fetch prompt from service
    await update.message.reply_text(
        f"""You've picked {context.chat_data["language"]} at {context.chat_data["CEFR"]} level. Good luck!"""
    )
    await update.message.reply_text(f"""Here's your prompt: INSERT PROMPT HERE""")
    return INPUT_USER_TEXT


async def grade_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends user text to LLM endpoint for grading."""
    await update.message.reply_text("Great job! Let's see how you did. 🧐")

    await update.message.reply_text(
        update.message.text
    )  # TODO: send user text to LLM endpoint for grading
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        """
    Use the following commands to interact with me:
    /start - Start the bot. 
          """
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give more information about Conversá to users."""
    await update.message.reply_text(
        """
        Conversá is your friendly language teacher! It'll give you a hand with your writing and give you feedback on your text. Developed by Hud Syafiq Herman and powered by LLMs 😁
        """
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye, see you later!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("insert token here").build()

    # adding the info command handlers (outside of main conversation flow)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # add main conversation flow handler with states
    main_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_LANGUAGE: [
                MessageHandler(filters.Regex("^(Spanish|French)$"), select_CEFR_level)
            ],
            SELECT_CEFR_LEVEL: [
                MessageHandler(
                    filters.Regex("^(A1|A2|B1|B2|C1|C2)$"), issue_writing_prompt
                )
            ],
            INPUT_USER_TEXT: [MessageHandler(filters.TEXT, grade_user_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(main_conversation_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
