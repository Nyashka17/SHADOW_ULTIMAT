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
import aiohttp
import os
import shutil
from datetime import datetime


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
        pass

    def get_current_version(self):
        """Получить текущую версию модуля"""
        try:
            # Импорт версии из основного модуля
            from ..Shadow_Ultimat import __version__
            return '.'.join(map(str, __version__))
        except Exception as e:
            logger.error(f"Error getting version: {e}")
            return "unknown"

    async def check_github_updates(self):
        """Проверяет обновления на GitHub"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.github.com/repos/Nyashka17/SHADOW_ULTIMAT/releases/latest"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        latest_version = data.get('tag_name', '').lstrip('v')

                        current = self.get_current_version()
                        if self.version_compare(latest_version, current) > 0:
                            return {
                                'available': True,
                                'version': latest_version,
                                'changelog': data.get('body', ''),
                                'url': data.get('html_url', '')
                            }
        except Exception as e:
            logger.error(f"Error checking updates: {e}")
        return {'available': False}

    def version_compare(self, v1, v2):
        """Сравнивает версии"""
        def parse_version(v):
            return tuple(map(int, v.split('.')))

        try:
            return parse_version(v1) > parse_version(v2)
        except:
            return False

    async def create_backup(self):
        """Создаёт резервную копию"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"sh_backup_{timestamp}"

        try:
            os.makedirs(backup_dir, exist_ok=True)

            files_to_backup = [
                'Shadow_Ultimat.py',
                'libs/shadowlib.py',
                'translations/Shadow_Ultimat.yml'
            ]

            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    dest_path = os.path.join(backup_dir, file_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(file_path, dest_path)

            return backup_dir
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

    async def download_files(self, version):
        """Скачивает файлы модуля с GitHub"""
        base_url = f"https://raw.githubusercontent.com/Nyashka17/SHADOW_ULTIMAT/{version}"

        files_to_download = [
            'Shadow_Ultimat.py',
            'libs/shadowlib.py',
            'translations/Shadow_Ultimat.yml'
        ]

        try:
            async with aiohttp.ClientSession() as session:
                for file_path in files_to_download:
                    url = f"{base_url}/{file_path}"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            content = await resp.text()
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error downloading files: {e}")
            return False

    async def update_module(self, version, call=None):
        """Обновляет модуль"""
        try:
            # Создать бэкап
            backup = await self.create_backup()
            if not backup:
                return "❌ Не удалось создать резервную копию"

            # Скачать файлы
            if not await self.download_files(f"v{version}"):
                return "❌ Не удалось скачать обновление"

            # Перезагрузить модуль (если возможно)
            # В Hikka это может потребовать перезапуска

            return f"✅ Модуль обновлён до версии {version}\nРезервная копия: {backup}"

        except Exception as e:
            logger.error(f"Error updating module: {e}")
            return f"❌ Ошибка обновления: {str(e)}"

    async def get_available_versions(self):
        """Получить список всех доступных версий с GitHub"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.github.com/repos/Nyashka17/SHADOW_ULTIMAT/releases"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        releases = await resp.json()
                        versions = []
                        for release in releases:
                            tag = release.get('tag_name', '').lstrip('v')
                            if tag and self.is_valid_version(tag):
                                versions.append({
                                    'version': tag,
                                    'name': release.get('name', ''),
                                    'body': release.get('body', ''),
                                    'published_at': release.get('published_at', ''),
                                    'url': release.get('html_url', '')
                                })
                        # Сортировать по версии (новые сверху)
                        versions.sort(key=lambda x: self.parse_version(x['version']), reverse=True)
                        return versions
        except Exception as e:
            logger.error(f"Error getting versions: {e}")
        return []

    def is_valid_version(self, version_str):
        """Проверить валидность версии (6 компонентов)"""
        try:
            parts = version_str.split('.')
            return len(parts) == 6 and all(part.isdigit() for part in parts)
        except:
            return False

    def parse_version(self, version_str):
        """Парсить версию в tuple для сортировки"""
        try:
            return tuple(map(int, version_str.split('.')))
        except:
            return (0, 0, 0, 0, 0, 0)

    def get_available_backups(self):
        """Получить список доступных бэкапов"""
        try:
            backups = []
            for item in os.listdir('.'):
                if item.startswith('sh_backup_') and os.path.isdir(item):
                    backups.append(item)
            # Сортировать по дате (новые сверху)
            backups.sort(reverse=True)
            return backups
        except Exception as e:
            logger.error(f"Error getting backups: {e}")
            return []

    async def rollback_to_backup(self, backup_dir):
        """Откат к указанному бэкапу"""
        try:
            if not os.path.exists(backup_dir):
                return "❌ Бэкап не найден"

            # Создать бэкап текущего состояния перед откатом
            current_backup = await self.create_backup()
            if not current_backup:
                return "❌ Не удалось создать бэкап перед откатом"

            # Восстановить файлы из бэкапа
            files_to_restore = [
                'Shadow_Ultimat.py',
                'libs/shadowlib.py',
                'translations/Shadow_Ultimat.yml'
            ]

            for file_path in files_to_restore:
                backup_path = os.path.join(backup_dir, file_path)
                if os.path.exists(backup_path):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    shutil.copy2(backup_path, file_path)

            return f"✅ Откат выполнен\nБэкап текущего состояния: {current_backup}"

        except Exception as e:
            logger.error(f"Error rolling back: {e}")
            return f"❌ Ошибка отката: {str(e)}"

    async def install_specific_version(self, version):
        """Установить конкретную версию"""
        try:
            # Создать бэкап
            backup = await self.create_backup()
            if not backup:
                return "❌ Не удалось создать резервную копию"

            # Скачать файлы указанной версии
            if not await self.download_files(f"v{version}"):
                return "❌ Не удалось скачать версию"

            return f"✅ Версия {version} установлена\nРезервная копия: {backup}"

        except Exception as e:
            logger.error(f"Error installing version: {e}")
            return f"❌ Ошибка установки: {str(e)}"
