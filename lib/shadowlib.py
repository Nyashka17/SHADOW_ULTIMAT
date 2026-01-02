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

from telethon.errors.rpcerrorlist import (
    UserNotParticipantError,
    HideRequesterMissingError,
)
from telethon.functions import messages, channels
from telethon import types

from .. import loader, utils
from ..types import SelfUnload

logger = logging.getLogger("ShadowLib")


class ShadowLib(loader.Library):
    """Custom library for Shadow modules."""

    developer = "@shadow_mod777"

    strings = {
        "name": "ShadowLib",
        "desc": "Custom library for Shadow modules.",
        "request_join_reason": "Stay tuned for updates.",
    }

    async def init(self):
        self.version = VersionUtils()

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            logger.info(f"Unloaded library: {name}")
            return True
        return False

    @classmethod
    async def only_legacy(cls):
        if not __package__.startswith("legacy"):
            raise loader.SelfUnload("The module is supported ONLY for Legacy userbot")


class VersionUtils:
    async def check_version(self):
        try:
            url = "https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/main/Shadow_Ultimat.py"
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                match = re.search(r'__version__\s*=\s*\(([^)]+)\)', content)
                if match:
                    remote_version = tuple(map(int, match.group(1).split(',')))
                    return remote_version
        except Exception as e:
            logger.error(f"Failed to check version: {e}")
        return None

    async def update_module(self, client, module_file, strings):
        try:
            url = "https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/main/Shadow_Ultimat.py"
            with urllib.request.urlopen(url) as response:
                new_content = response.read().decode('utf-8')
            with open(module_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            await client.send_message("me", strings["update_success"])
            # Reload module if possible
            # Assuming self.allmodules is available
            await self.allmodules.reload("Shadow_Ultimat")
        except Exception as e:
            await client.send_message("me", strings["update_failed"].format(str(e)))

    def version_history(self):
        # Moved to module strings
        return {}
