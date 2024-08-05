import logging
import sys
import os

from .factory import create_bot


os.environ["BOT_TOKEN"] = "7327176732:AAHaVo-2KGNDNlxJzcTnG6ZOqvAq_MkhqGI"
bot = create_bot()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot.run_polling()
