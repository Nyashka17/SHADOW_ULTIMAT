#  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗███████╗███████╗
# ██╔═════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║     ████╗ ████║██╔═══██╗██╔══██╗╚════██║╚════██║╚════██║
# ███████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║     ██╔████╔██║██║   ██║██║  ██║    ██╔╝    ██╔╝    ██╔╝
#  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║     ██║╚██╔╝██║██║   ██║██║  ██║   ██╔╝    ██╔╝    ██╔╝ 
# ███████║ ██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╝      ██║ ╚═╝ ██║╚██████╔╝██████╔╝  ██╔╝    ██╔╝    ██╔╝  
# ╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ █████╗╚═╝     ╚═╝ ╚═════╝ ╚═════╝   ╚═╝     ╚═╝     ╚═╝   


__version__ = (7, 7, 7, 0, 2, 4)
# meta developer: @shadow_mod777
# scope: disable_onload_docs
# packurl: https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/refs/heads/main/tr/Shadow_Ultimat.yml

import logging
import json
import urllib.request
import time
import asyncio
import typing
import re
import html
from telethon.tl.functions.messages import ReadMentionsRequest
from telethon.tl.functions.channels import InviteToChannelRequest, EditAdminRequest
from telethon.tl.types import ChatAdminRights

from ..inline.types import InlineCall
from ..types import SelfUnload

# Настройка логирования
logger = logging.getLogger(__name__)

@loader.tds
class Shadow_Ultimat(loader.Module):
    """Афто фарм Бфгб от #тени"""

    strings = {
        "name": "Shadow_Ultimat",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.prefix = self.db.get("hikka.main", "command_prefix", None) or self.db.get(
            "heroku.main", "command_prefix", "."
        )
        self.shadowlib = await self.import_lib(
            "https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/main/lib/shadowlib.py",
            suspend_on_error=True,
        )

    def version_history(self):
        return self.strings["version_history"]

    async def check_version(self):
        return await self.shadowlib.check_version()

    async def update_module(self):
        await self.shadowlib.update_module(self.client, __file__, self.strings)

    async def версияcmd(self, message):
        """Show module version and history."""
        current = '.'.join(map(str, __version__))
        desc = self.strings["description"]
        text = f"{self.strings['current_version'].format(current)}\n{desc}\n\n"

        remote = await self.check_version()
        if remote and remote > __version__:
            remote_str = '.'.join(map(str, remote))
            text += f"{self.strings['update_available'].format(remote_str)}\n"
            # Add update button
            await self.inline.form(
                text=text,
                message=message,
                reply_markup=[
                    [{"text": "Update", "callback": self.update_callback}],
                    [{"text": self.strings["version_history"], "callback": self.history_callback, "args": (0,)}],
                ]
            )
        else:
            text += self.strings["no_update"] + "\n"
            await self.inline.form(
                text=text,
                message=message,
                reply_markup=[
                    [{"text": self.strings["version_history"], "callback": self.history_callback, "args": (0,)}],
                ]
            )

    async def history_callback(self, call: InlineCall, page: int = 0):
        history = self.version_history()
        versions = list(history.keys())[::-1]  # Newest first
        per_page = 5
        start = page * per_page
        end = start + per_page
        current_versions = versions[start:end]

        text = self.strings["version_history"] + ":\n\n"
        for ver in current_versions:
            text += f"<b>{ver}</b>: {history[ver]}\n"

        buttons = []
        if page > 0:
            buttons.append({"text": self.strings["prev"], "callback": self.history_callback, "args": (page - 1,)})
        if end < len(versions):
            buttons.append({"text": self.strings["next"], "callback": self.history_callback, "args": (page + 1,)})
        buttons.append({"text": self.strings["back"], "callback": self.back_to_version})

        await call.edit(text, reply_markup=[buttons])

    async def back_to_version(self, call: InlineCall):
        await self.версияcmd(call.message)

    async def update_callback(self, call: InlineCall):
        await call.edit(self.strings["updating"])
        await self.update_module()

    async def cleardbcmd(self, message):
        """Clear module database."""
        # Clear all keys related to this module
        module_prefix = self.__class__.__name__.lower()
        keys_to_remove = [k for k in self.db if k.startswith(module_prefix)]
        for k in keys_to_remove:
            del self.db[k]
        await utils.answer(message, self.strings["db_cleared"])
