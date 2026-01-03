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

    developer = "@shadow_mod777"

    strings = {
        "name": "ShadowLib",
        "desc": "Custom library for Shadow modules.",
        "request_join_reason": "Stay tuned for updates.",
        "not_legacy": "The module is supported only on <a href='https://github.com/Crayz310/Legacy'>{label}</a>",
    }

    async def init(self):
        self.version = VersionUtils()
        self.version_update_check()

    @classmethod
    async def only_legacy(self):
        if not __package__.startswith("legacy"):
            raise SelfUnload("The module is supported ONLY for Legacy userbot")

    def unload_lib(self, name: str):
        instance = self.lookup(name)
        if isinstance(instance, loader.Library):
            self.allmodules.libraries.remove(instance)
            logger.info(f"Unloaded library: {name}")
            return True
        return False
    
class VersionUtils:
    """Utility class for version handling."""

    def __init__(self):
        self.version = (7, 7, 7, 0, 0, 1)
        self.version_info = {
            "7.7.7.0.0.1": {
                "ru": "📝 Была добавлена лаба в модуль (📚shadowlib).",
                "en": "📝 A lab was added to the module (📚shadowlib)."
            },
            "7.7.7.0.0.2": {
                "ru": "📝 Проверка работоспособности переходов на новую версию, добавлен список версий (📜 История).",
                "en": "📝 Checking the functionality of transitions to a new version, added a list of versions (📜 History)."
            }
        }
        self.github_repo = "https://github.com/Nyashka17/SHADOW_ULTIMAT"
        self.versions = [
            {
                "version": "7.7.7.0.0.1",
                "commit_link": "https://github.com/Nyashka17/SHADOW_ULTIMAT/commit/abc123",
                "status": "✅",
                "files": [
                    "lib/shadowlib.py",
                    "tr/Shadow_Ultimat.yml",
                    "Shadow_Ultimat.py"
                ]
            },
            {
                "version": "7.7.7.0.0.2", 
                "commit_link": "https://github.com/Nyashka17/SHADOW_ULTIMAT/commit/def456",
                "status": "🌀",
                "files": [
                    "lib/shadowlib.py",
                    "tr/Shadow_Ultimat.yml", 
                    "Shadow_Ultimat.py"
                ]
            }
        ]

    def get_version(self) -> str:
        return ".".join(map(str, self.version))
    
    def get_version_tuple(self) -> tuple:
        return self.version
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """Compare two version strings. Returns 1 if version1 > version2, -1 if version1 < version2, 0 if equal."""
        v1_parts = tuple(map(int, version1.split('.')))
        v2_parts = tuple(map(int, version2.split('.')))
        
        if v1_parts > v2_parts:
            return 1
        elif v1_parts < v2_parts:
            return -1
        else:
            return 0
    
    def is_update_available(self, current_version: str, latest_version: str) -> bool:
        """Check if update is available."""
        return self.compare_versions(latest_version, current_version) > 0
    
    def get_version_info(self, version: str, lang: str = "en") -> str:
        """Get version information."""
        if version in self.version_info:
            return self.version_info[version].get(lang, self.version_info[version]["en"])
        return f"Version {version} information not available."
    
    def get_latest_version(self) -> str:
        """Get the latest version from the list."""
        if self.versions:
            return self.versions[-1]["version"]
        return self.get_version()
    
    def get_version_history(self, page: int = 1, page_size: int = 5):
        """Get version history with pagination."""
        total_pages = (len(self.versions) + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        if page < 1 or start_idx >= len(self.versions):
            return [], 0, 0
        
        paginated_versions = self.versions[start_idx:end_idx]
        return paginated_versions, page, total_pages
    
    def format_version_tree(self, version_data: list) -> str:
        """Format version data as a tree structure."""
        if not version_data:
            return "No versions available."
        
        tree_lines = []
        for i, ver in enumerate(version_data):
            prefix = "├── " if i < len(version_data) - 1 else "└── "
            tree_lines.append(f"{prefix}v{ver['version']}/ {ver['commit_link']}")
            
            for file_path in ver['files']:
                file_prefix = "│   " if i < len(version_data) - 1 else "    "
                file_status = ver['status']
                tree_lines.append(f"{file_prefix}└── {file_path} {file_status}")
        
        # Add footer
        tree_lines.append("├─────────────")
        tree_lines.append(f"├── link/ → {self.github_repo}")
        tree_lines.append("└── archive/")
        tree_lines.append("    └── main v0.0.1/")
        tree_lines.append("    └── beta v0.0.1/")
        
        return "\n".join(tree_lines)
    
class VersionCheck:
    """Custom exception for version check."""
    pass
    def version_update_check(self):
        # Placeholder for version update check logic
        pass
        # Here you can implement the logic to check for updates
        # and raise VersionCheck exception if needed
        # For example:
        # latest_version = self.fetch_latest_version()
        # if self.version.get_version() < latest_version:
        #     raise VersionCheck("A new version is available.")
    def fetch_latest_version(self) -> str:
        # Placeholder for fetching the latest version from a remote source
        return "7.7.7"
        # You can implement the actual fetching logic here if needed
