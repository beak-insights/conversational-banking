import os

from chatgpt_md_converter import telegram_format
from telegram import Update
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes,
    MessageHandler,
    filters
)

from banking import seed_for_user
from .session import get_session

CWD = os.path.join(os.path.dirname(__file__))
TOKEN = os.getenv("TELEGRAM_API_KEY")

app = ApplicationBuilder().token(TOKEN).build()


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This handler receives messages with `/start` command
    """
    session = await get_session(update.message.from_user)
    await app.bot.send_chat_action(update.message.chat.id, "typing")
    resp = await session["agent"].aprompt(f"Hie, who are and how can you be helped today?")
    await update.message.reply_text(resp)


async def commdand_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Beak Bank help section:\n"
    )

async def commdand_seed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs a simulation of the bank assistant in the context of the user."""
    user = update.message.from_user
    await update.message.reply_text("Seeding your starter banking data...")
    await app.bot.send_chat_action(update.message.chat.id, "typing")
    seed_for_user(str(user.id), user.full_name)
    await get_session(update.effective_user, has_context=True)
    await update.message.reply_text(
        "Bank Accounts initialized successfully."
    )

async def comand_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages to the agent.
    """
    session = await get_session(update.effective_user, has_context=True)
    # try:
    chat = update.effective_chat
    assert update.effective_user == update.message.from_user
    assert  update.effective_message == update.message
    await app.bot.send_chat_action(chat.id, "typing")
    resp = await session["agent"].aprompt(update.message.text)
    as_html = telegram_format(resp)
    await update.message.reply_text(as_html, parse_mode='HTML')
    # except Exception as e:
    #     # error or handle it somehow
    #     await update.message.reply_text(f"Sorry An error occured >> {str(e)}")
    #     # reset the agent
    #     session["agent"].init()


app.add_handler(CommandHandler("start", command_start))
app.add_handler(CommandHandler("seed", commdand_seed))
app.add_handler(CommandHandler("help", commdand_help))
app.add_handler(MessageHandler(filters.ALL, comand_message))


def poll() -> None:
    # And the run events dispatching
    app.run_polling()
