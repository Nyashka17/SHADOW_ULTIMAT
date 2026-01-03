#  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗███████╗███████╗
# ██╔═════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║     ████╗ ████║██╔═══██╗██╔══██╗╚════██║╚════██║╚════██║
# ███████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║     ██╔████╔██║██║   ██║██║  ██║    ██╔╝    ██╔╝    ██╔╝
#  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║     ██║╚██╔╝██║██║   ██║██║  ██║   ██╔╝    ██╔╝    ██╔╝ 
# ███████║ ██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╝      ██║ ╚═╝ ██║╚██████╔╝██████╔╝  ██╔╝    ██╔╝    ██╔╝  
# ╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ █████╗╚═╝     ╚═╝ ╚═════╝ ╚═════╝   ╚═╝     ╚═╝     ╚═╝   


__version__ = (7, 7, 7, 0, 0, 1)
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
            "https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/refs/heads/main/lib/shadowlib.py",
            suspend_on_error=True,
        )
        self.prefix = self.db.get("hikka.main", "command_prefix", None) or self.db.get(
            "heroku.main", "command_prefix", "."
        )

 
    async def версияcmd(self, message):
        """менеджер версиями."""
        await self.show_version_info(message)
    
    async def show_version_info(self, message):
        """Show version information with inline buttons."""
        current_version = self.shadowlib[0].version.get_version()
        latest_version = self.shadowlib[0].version.get_latest_version()
        
        # Check if update is available
        update_available = self.shadowlib[0].version.is_update_available(current_version, latest_version)
        
        # Create version display
        version_display = f"🇻‌🇪‌🇷‌🇸‌🇮‌🇴‌🇳‌: [{', '.join(map(str, self.shadowlib[0].version.get_version_tuple()))}]"
        
        if update_available:
            status_text = f"♨️: Доступно обновление до {latest_version}!"
            info_text = self.strings("version_update_info").format(version=latest_version)
            version_info = self.shadowlib[0].version.get_version_info(latest_version, "ru")
        else:
            status_text = "✅: Актуальная версия!"
            info_text = self.strings("version_info").format(version=current_version)
            version_info = self.shadowlib[0].version.get_version_info(current_version, "ru")
        
        # Create message text
        message_text = f"<blockquote>{version_display}</blockquote>\n\n{status_text}\n\n{info_text}\n\n{version_info}\n\n-- Хотите обновиться зайдите в раздел обновлений --</blockquote>"
        
        # Create inline buttons
        buttons = [
            [{"text": self.strings("updates_button"), "callback": self.show_updates}],
            [{"text": self.strings("history_button"), "callback": self.show_history}]
        ]
        
        await self.inline.form(
            message=message,
            text=message_text,
            reply_markup=buttons,
            **{"disable_security": True}
        )
    
    async def show_updates(self, call: InlineCall):
        """Show updates section."""
        current_version = self.shadowlib[0].version.get_version()
        latest_version = self.shadowlib[0].version.get_latest_version()
        
        update_available = self.shadowlib[0].version.is_update_available(current_version, latest_version)
        
        if update_available:
            message_text = f"<blockquote>{self.strings('new_update_available')}</blockquote>\n\n{self.strings('use_button_below')} <i>⚜️ {latest_version} </i>⚜️ ..."
            buttons = [
                [{"text": self.strings("update_to_version").format(version=latest_version), "callback": self.perform_update}]
            ]
        else:
            message_text = f"<blockquote>{self.strings('last_version')}</blockquote>\n\n{self.strings('no_update_needed')}"
            buttons = []
        
        await call.edit(
            text=message_text,
            reply_markup=buttons
        )
    
    async def show_history(self, call: InlineCall, page: int = 1):
        """Show version history with pagination."""
        version_data, current_page, total_pages = self.shadowlib[0].version.get_version_history(page)
        
        if not version_data:
            message_text = self.strings("no_versions")
            buttons = []
        else:
            tree_display = self.shadowlib[0].version.format_version_tree(version_data)
            message_text = f"<blockquote>{self.strings('version_list')}</blockquote>\n\n{tree_display}\n\n{self.strings('page_info').format(current=current_page, total=total_pages)}"
            
            buttons = []
            if total_pages > 1:
                row = []
                if current_page > 1:
                    row.append({"text": self.strings("prev"), "callback": lambda: self.show_history(call, page - 1)})
                if current_page < total_pages:
                    row.append({"text": self.strings("next"), "callback": lambda: self.show_history(call, page + 1)})
                if row:
                    buttons.append(row)
            
            # Add version detail buttons
            for ver in version_data:
                buttons.append([{
                    "text": self.strings("version_button").format(version=ver["version"]),
                    "callback": lambda ver=ver: self.show_version_details(call, ver["version"])
                }])
        
        await call.edit(
            text=message_text,
            reply_markup=buttons
        )
    
    async def show_version_details(self, call: InlineCall, version: str):
        """Show detailed information about a specific version."""
        version_info = self.shadowlib[0].version.get_version_info(version, "ru")
        message_text = f"<blockquote>{self.strings('version_details_info').format(version=version)}</blockquote>\n\n{version_info}"
        
        buttons = [[{"text": self.strings("back"), "callback": self.show_history}]]
        
        await call.edit(
            text=message_text,
            reply_markup=buttons
        )
    
    async def perform_update(self, call: InlineCall):
        """Perform the update (placeholder for actual update logic)."""
        # This would contain the actual update logic
        await call.edit("Updating...")
        # Simulate update process
        await asyncio.sleep(2)
        await call.edit("Update completed!")
