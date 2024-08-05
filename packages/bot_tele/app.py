import logging
import sys
import os

from .factory import create_bot


BOT_TOKEN = os.environ["TELEGRAM_API_KEY"]
bot = create_bot()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot.run_polling()
