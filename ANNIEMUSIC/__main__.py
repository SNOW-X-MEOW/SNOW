import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ANNIEMUSIC import LOGGER, app, userbot
from ANNIEMUSIC.core.call import JARVIS
from ANNIEMUSIC.misc import sudo
from ANNIEMUSIC.plugins import ALL_MODULES
from ANNIEMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Check assistant sessions
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "ᴀssɪsᴛᴀɴᴛ sᴇssɪᴏɴ ɴᴏᴛ ғɪʟʟᴇᴅ, "
            "ᴘʟᴇᴀsᴇ ғɪʟʟ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ..."
        )
        return

    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except Exception as e:
        LOGGER(__name__).warning(
            f"Failed to load banned users: {e}"
        )

    # Main bot
    await app.start()

    # Plugins
    for all_module in ALL_MODULES:
        importlib.import_module(
            "ANNIEMUSIC.plugins" + all_module
        )

    LOGGER("ANNIEMUSIC.plugins").info(
        "ʙʀᴏᴋᴇɴ x ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ..."
    )

    # Assistant
    await userbot.start()

    # Music bot
    await JARVIS.start()

    # Voice chat test
    try:
        await JARVIS.stream_call(
            "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
        )

    except NoActiveGroupCall:
        LOGGER("MUSICBROKN").error(
            "ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ "
            "ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n\n"
            "ᴀɴɴɪᴇ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ..."
        )
        return

    except Exception as e:
        LOGGER("MUSICBROKN").error(
            f"Voice chat startup failed: {type(e).__name__}: {e}"
        )

    await JARVIS.decorators()

    LOGGER("MUSICBROKN").info(
        "Annie Music Robot Started Successfully..."
    )

    await idle()

    # Clean shutdown
    try:
        await app.stop()
    except Exception:
        pass

    try:
        await userbot.stop()
    except Exception:
        pass

    try:
        await JARVIS.stop()
    except Exception:
        pass

    LOGGER("MUSICBROKN").info(
        "sᴛᴏᴘɪɴɢ ʙʀᴏᴋᴇɴ x ᴍᴜsɪᴄ ʙᴏᴛ ..."
    )


if __name__ == "__main__":
    asyncio.run(init())
