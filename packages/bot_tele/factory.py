import os

from telegram.ext import (
    ApplicationBuilder, 
    Application,
    CommandHandler, 
    MessageHandler,
    filters
)

from .handlers import (
    command_start,
    commdand_help,
    comand_message
)


def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", command_start))
    app.add_handler(CommandHandler("help", commdand_help))
    app.add_handler(MessageHandler(filters.TEXT, comand_message))


def create_bot() -> Application:
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    register_handlers(app)
    return app
