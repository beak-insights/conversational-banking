import logging
import sys
import os
import asyncio

from bot.aiog import poll as aiog_poll
from bot.ptg import poll as ptg_poll

# Bot token can be obtained via https://t.me/BotFather

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # asyncio.run(aiog_poll())
    ptg_poll()
