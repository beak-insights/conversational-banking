from typing import NoReturn

from chatgpt_md_converter import telegram_format
from telegram import Update
from telegram.ext import ContextTypes

from .session import (
    init_session,
    get_session, 
    update_session
)
from .service import (
    bank_post,
    assistant_post
)



async def commdand_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
    """Displays info on how to use the bot."""
    await context.bot.send_chat_action(update.message.chat.id, "typing")
    resp = await assistant_post("/ask", update.message.from_user, "What kind of questions can you help me with? Help me understand how to use you. \
                                Give examples of all possible question i can ask")
    as_html = telegram_format(resp)
    await update.message.reply_text(as_html, parse_mode='HTML')


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
    """
    This handler receives messages with `/start` command
    """
    await init_session(update.message.from_user)
    await context.bot.send_chat_action(update.message.chat.id, "typing")
    resp = await assistant_post("/ask", update.message.from_user, "Hie, who are and how can you be help me?")    
    as_html = telegram_format(resp)
    await update.message.reply_text(as_html, parse_mode='HTML')


async def comand_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
    """Handle messages to the agent.
    """
    session = await get_session(update.effective_user)
    # try:
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    resp = await assistant_post("/ask", update.message.from_user, update.message.text)
    as_html = telegram_format(resp)
    await update.message.reply_text(as_html, parse_mode='HTML')
    # except Exception as e:
    #     # error or handle it somehow
    #     await update.message.reply_text(f"Sorry An error occured >> {str(e)}")
    #     # reset the agent
    #     session["agent"].init()


async def commdand_seed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> NoReturn:
    """Seed starter data for a user."""
    user = update.message.from_user
    await update.message.reply_text("Seeding your starter banking data...")
    await context.bot.send_chat_action(update.message.chat.id, "typing")
    resp = await bank_post("/seed", {"user_id": str(user.id), "full_name": user.full_name})
    await update_session(update.effective_user, user_context=resp["context"])
    await update.message.reply_text("Bank Accounts initialized successfully.")
