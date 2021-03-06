# Copyright (C) 2021 By WoofMusic

from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import Woof
from helpers.decorators import sudo_users_only
from helpers.filters import command

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{Woof.BOT_USERNAME}"]))
async def start(_, m: Message):
    if m.chat.type == "private":
        await m.reply_text(
            f"āØ **Hello there, I am a telegram group video streaming bot.**\n\nš­ **I was created to stream videos in group "
            f"video chats easily.**\n\nā **To find out how to use me, please press the help button below** šš»",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "ā Add me to your Group ā", url=f"https://t.me/{Woof.BOT_USERNAME}?startgroup=true")
                ], [
                    InlineKeyboardButton(
                        "ā HOW TO USE THIS BOT", callback_data="cbguide")
                ], [
                    InlineKeyboardButton(
                        "š Terms & Condition", callback_data="cbinfo")
                ], [
                    InlineKeyboardButton(
                        "š¬ Group", url="https://t.me/mailmusicupdate"),
                    InlineKeyboardButton(
                        "š£ Channel", url="https://t.me/mailmusicupdate")
                ], [
                    InlineKeyboardButton(
                        "š©š»āš» Developer", url="https://t.me/mailmusicupdate")
                ], [
                    InlineKeyboardButton(
                        "š All Command List", callback_data="cblist")
                ]]
            ))
    else:
        await m.reply_text("**āØ Woof is online now āØ**",
                           reply_markup=InlineKeyboardMarkup(
                               [[
                                   InlineKeyboardButton(
                                       "ā HOW TO USE THIS BOT", callback_data="cbguide")
                               ], [
                                   InlineKeyboardButton(
                                       "š Search Youtube", switch_inline_query='')
                               ], [
                                   InlineKeyboardButton(
                                       "š Command List", callback_data="cblist")
                               ]]
                           )
                           )


@Client.on_message(command(["alive", f"alive@{Woof.BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def alive(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"""ā **Woof is running**\n<b>š  **uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "āØ Group", url=f"https://t.me/mailmusicupdate"
                    ),
                    InlineKeyboardButton(
                        "š£ Channel", url=f"https://t.me/mailmusicupdate"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{Woof.BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(_, m: Message):
    sturt = time()
    m_reply = await m.reply_text("pinging...")
    delta_ping = time() - sturt
    await m_reply.edit_text(
        "š `Woof!!`\n"
        f"ā”ļø `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{Woof.BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "š¤ Woof status š¤\n\n"
        f"ā¢ **uptime:** `{uptime}`\n"
        f"ā¢ **start time:** `{START_TIME_ISO}`"
    )
