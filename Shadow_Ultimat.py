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

    @loader.command()
    async def версия(self, message):
        """Проверяет версию модуля и предлагает обновление"""
        updates = await self.shadowlib.updater.check_github_updates()

        if updates['available']:
            # Показать inline форму
            await self.inline.form(
                message=message,
                text=f"📦 Доступна новая версия: {updates['version']}\n\n"
                     f"📝 Изменения:\n{updates['changelog'][:300]}...",
                reply_markup=[
                    {
                        "text": "🔄 Обновить",
                        "callback": self.update_module_callback,
                        "args": (updates['version'],)
                    },
                    {"text": "❌ Отмена", "action": "close"}
                ]
            )
        else:
            current_version = self.shadowlib.version_mgr.get_current_version()
            await utils.answer(message, f"✅ Текущая версия: {current_version}\nОбновлений нет.")

    async def update_module_callback(self, call, version):
        """Callback для обновления модуля"""
        await utils.answer(call, "🔄 Обновляю модуль...")

        result = await self.shadowlib.updater.update_module(version)

        await utils.answer(call, result)

    @loader.command()
    async def версии(self, message):
        """Панель управления версиями модуля"""
        current_version = self.shadowlib.version_mgr.get_current_version()
        updates = await self.shadowlib.updater.check_github_updates()
        backups = self.shadowlib.backuper.get_available_backups()

        text = f"📋 Управление версиями\n\nТекущая версия: {current_version}"

        if updates['available']:
            text += f"\n\n🔄 Доступна версия: {updates['version']}"

        if backups:
            text += f"\n\n🔙 Доступно бэкапов: {len(backups)}"

        markup = [
            [
                {
                    "text": "🔄 Обновить",
                    "callback": self.show_update_menu,
                    "args": ()
                },
                {
                    "text": "📦 Выбрать версию",
                    "callback": self.show_versions_list,
                    "args": (0,)  # page 0
                }
            ],
            [
                {
                    "text": f"🔙 Откат ({len(backups)})",
                    "callback": self.show_backups_menu,
                    "args": ()
                },
                {
                    "text": "ℹ️ Инфо",
                    "callback": self.show_version_info,
                    "args": ()
                }
            ]
        ]

        await self.inline.form(
            message=message,
            text=text,
            reply_markup=markup
        )

    async def show_update_menu(self, call):
        """Показать меню обновления"""
        updates = await self.shadowlib.updater.check_github_updates()

        if not updates['available']:
            await utils.answer(call, "✅ Обновлений нет")
            return

        text = f"🔄 Обновление до версии {updates['version']}\n\n📝 Изменения:\n{updates['changelog'][:300]}..."

        markup = [
            {
                "text": "✅ Обновить",
                "callback": self.update_module_callback,
                "args": (updates['version'],)
            },
            {"text": "❌ Отмена", "action": "close"}
        ]

        await self.inline.form(
            call=call,
            text=text,
            reply_markup=markup
        )

    async def show_versions_list(self, call, page=0):
        """Показать список доступных версий"""
        versions = await self.shadowlib.github.get_available_versions()
        current = self.shadowlib.version_mgr.get_current_version()

        if not versions:
            await utils.answer(call, "❌ Не удалось получить список версий")
            return

        # Пагинация: 5 версий на страницу
        per_page = 5
        start = page * per_page
        end = start + per_page
        page_versions = versions[start:end]

        text = f"📦 Доступные версии (страница {page + 1})\n\nТекущая: {current}\n"

        markup = []
        for v in page_versions:
            status = "✅" if v['version'] == current else "⬜"
            markup.append([
                {
                    "text": f"{status} {v['version']}",
                    "callback": self.show_version_details,
                    "args": (v['version'],)
                }
            ])

        # Кнопки навигации
        nav_buttons = []
        if page > 0:
            nav_buttons.append({
                "text": "⬅️ Назад",
                "callback": self.show_versions_list,
                "args": (page - 1,)
            })

        if end < len(versions):
            nav_buttons.append({
                "text": "Вперёд ➡️",
                "callback": self.show_versions_list,
                "args": (page + 1,)
            })

        if nav_buttons:
            markup.append(nav_buttons)

        markup.append([{"text": "❌ Закрыть", "action": "close"}])

        await self.inline.form(
            call=call,
            text=text,
            reply_markup=markup
        )

    async def show_version_details(self, call, version):
        """Показать детали версии"""
        versions = await self.shadowlib.github.get_available_versions()
        version_info = next((v for v in versions if v['version'] == version), None)

        if not version_info:
            await utils.answer(call, "❌ Версия не найдена")
            return

        text = f"📦 Версия {version}\n\n📝 {version_info['body'][:500]}...\n\n🔗 {version_info['url']}"

        markup = [
            {
                "text": "✅ Установить",
                "callback": self.install_version_callback,
                "args": (version,)
            },
            {
                "text": "⬅️ Назад",
                "callback": self.show_versions_list,
                "args": (0,)
            },
            {"text": "❌ Закрыть", "action": "close"}
        ]

        await self.inline.form(
            call=call,
            text=text,
            reply_markup=markup
        )

    async def install_version_callback(self, call, version):
        """Установить выбранную версию"""
        await utils.answer(call, f"🔄 Устанавливаю версию {version}...")

        result = await self.shadowlib.updater.install_specific_version(version)

        await utils.answer(call, result)

    async def show_backups_menu(self, call):
        """Показать меню бэкапов"""
        backups = self.shadowlib.backuper.get_available_backups()

        if not backups:
            await utils.answer(call, "❌ Бэкапов не найдено")
            return

        text = f"🔙 Доступные бэкапы ({len(backups)})\n\nВыберите бэкап для отката:"

        markup = []
        for backup in backups[:5]:  # Показать первые 5
            timestamp = backup.replace('sh_backup_', '')
            markup.append([
                {
                    "text": f"📁 {timestamp}",
                    "callback": self.rollback_callback,
                    "args": (backup,)
                }
            ])

        markup.append([{"text": "❌ Закрыть", "action": "close"}])

        await self.inline.form(
            call=call,
            text=text,
            reply_markup=markup
        )

    async def rollback_callback(self, call, backup_dir):
        """Откат к бэкапу"""
        await utils.answer(call, f"🔄 Выполняю откат к {backup_dir}...")

        result = await self.shadowlib.backuper.rollback_to_backup(backup_dir)

        await utils.answer(call, result)

    async def show_version_info(self, call):
        """Показать информацию о версии"""
        current = self.shadowlib.version_mgr.get_current_version()
        backups = self.shadowlib.backuper.get_available_backups()

        text = f"ℹ️ Информация о версии\n\n📦 Текущая версия: {current}\n🔙 Бэкапов: {len(backups)}\n\nСхема версий: 7.7.7.X.X.X\nгде X изменяется последовательно"

        markup = [
            {
                "text": "⬅️ Назад",
                "callback": self.версии,
                "args": (call.message,)  # Передаём сообщение для формы
            },
            {"text": "❌ Закрыть", "action": "close"}
        ]

        await self.inline.form(
            call=call,
            text=text,
            reply_markup=markup
        )
