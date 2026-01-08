#  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗███████╗███████╗
# ██╔═════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║     ████╗ ████║██╔═══██╗██╔══██╗╚════██║╚════██║╚════██║
# ███████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║     ██╔████╔██║██║   ██║██║  ██║    ██╔╝    ██╔╝    ██╔╝
#  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║     ██║╚██╔╝██║██║   ██║██║  ██║   ██╔╝    ██╔╝    ██╔╝
# ███████║ ██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╝      ██║ ╚═╝ ██║╚██████╔╝██████╔╝  ██╔╝    ██╔╝    ██╔╝
# ╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ █████╗╚═╝     ╚═╝ ╚═════╝ ╚═════╝   ╚═╝     ╚═╝     ╚═╝

__version__ = (7, 7, 7, 0, 0, 0)
# meta developer: @shadow_mod777
# scope: disable_onload_docs
# packurl: https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/refs/heads/main/translations/Shadow_Ultimat.yml

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
from .. import loader, utils

# Настройка логирования
logger = logging.getLogger("Shadow_Ultimat")

@loader.tds
class Shadow_Ultimat(loader.Module):
    """Афто фарм Бфгб от #тени"""

    strings = {
        "name": "Shadow_Ultimat",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self.shadowlib = await self.import_lib(
            "https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/refs/heads/main/libs/shadowlib.py",
            suspend_on_error=True,
        )
        self.prefix = self.db.get("hikka.main", "command_prefix", None) or self.db.get(
            "heroku.main", "command_prefix", "."
        )

    async def init(self):
        pass