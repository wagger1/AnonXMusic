import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.errors import FloodWait

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


# ✅ Safe bot start that handles FloodWait
async def safe_start(bot):
    try:
        await bot.start()
    except FloodWait as e:
        LOGGER(__name__).error(f"🚫 FloodWait: Waiting {e.value} seconds before retrying...")
        await asyncio.sleep(e.value)
        await bot.start()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to load banned users: {e}")

    await safe_start(app)

    # ✅ Fixed plugin import
    for all_module in ALL_MODULES:
        if all_module.strip():
            try:
                importlib.import_module("AnonXMusic.plugins." + all_module.lstrip("."))
            except Exception as e:
                LOGGER("AnonXMusic.plugins").error(f"Failed to import {all_module}: {e}")

    LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Anony.start()

    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error(
            "❌ Please start a video chat in your log group/channel before launching the bot.\n\nStopping bot..."
        )
        exit()
    except Exception as e:
        LOGGER("AnonXMusic").warning(f"Stream setup skipped: {e}")

    await Anony.decorators()
    LOGGER("AnonXMusic").info(
        "AnonX Music Bot Started Successfully.\n\nDon't forget to visit @FallenAssociation."
    )

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("AnonXMusic").info("✅ Stopped AnonX Music Bot.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
