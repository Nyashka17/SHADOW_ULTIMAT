# This file is part of Shadow Mods.
# Custom library for Shadow modules.

# meta developer: @shadow_mod777

import logging
import json
import urllib.request
import time
import asyncio
import typing
import re
import html


from telethon.functions import messages, channels
from telethon import types

from .. import loader, utils
from ..types import SelfUnload

logger = logging.getLogger("ShadowLib")


class ShadowLib(loader.Library):
    """Custom library for Shadow modules."""

    developer = "custom.bot.tg@gmail.com"

    strings = {
        "name": "ShadowLib",
        "desc": "Custom library for Shadow modules.",
        "request_join_reason": "Stay tuned for updates.",
    }

    async def init(self):
        pass 