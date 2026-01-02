# This file is part of Shadow Mods.
# Custom library for Shadow modules.

# meta developer: @shadow_mod777

import logging
import typing

from ... import loader, utils

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
        # Initialize custom classes here as needed
        pass

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            logger.info(f"Unloaded library: {name}")
            return True
        return False

    # Add custom classes and functions here as needed

    @classmethod
    async def only_legacy(cls):
        if not __package__.startswith("legacy"):
            raise SelfUnload("The module is supported ONLY for Legacy userbot")

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            logger.info(f"Unloaded library: {name}")
            return True
        return False

    # Add custom classes and functions here as needed</content>
<parameter name="filePath">c:\Users\kozub\Desktop\SHADOW\Shadow_modules\main\SHADOW_ULTIMAT\shadowlib.py