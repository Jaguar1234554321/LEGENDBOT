import asyncio
import base64
import contextlib

from telethon.errors.rpcerrorlist import ForbiddenError
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers import media_type, unsavegif
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

menu_category = "extra"


async def spam_function(event, krishna, lol, sleeptimem, sleeptimet, DelaySpam=False):
    # sourcery skip: low-code-quality
    # sourcery no-metrics
    counter = int(lol[0])
    if len(lol) == 2:
        spam_message = str(lol[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await krishna.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and krishna.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            krishna = await event.client.send_file(
                event.chat_id, krishna, caption=krishna.text
            )
            await unsavegif(event, krishna)
            await asyncio.sleep(sleeptimem)
        if BOTLOG:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message",
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message with delay {sleeptimet} seconds",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message with delay {sleeptimet} seconds",
                )

            krishna = await event.client.send_file(BOTLOG_CHATID, krishna)
            await unsavegif(event, krishna)
        return
    elif event.reply_to_msg_id and krishna.text:
        spam_message = krishna.text
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat  with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
    elif BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )


@legend.legend_cmd(
    pattern="spam ([\s\S]*)",
    command=("spam", menu_category),
    info={
        "header": "Floods the text in the chat !! with given number of times.",
        "description": "Sends the replied media/message <count> times !! in the chat.",
        "note": "To stop the spam after starting it use '{tr}end spam' cmd.",
        "usage": ["{tr}spam <count> <text>", "{tr}spam <count> reply to message"],
        "examples": "{tr}spam 10 hi",
    },
)
async def spammer(event):
    "Floods the text in the chat !!"
    krishna = await event.get_reply_message()
    lol = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(lol[0])
    except Exception:
        return await eod(
            event, "__Use proper syntax to spam. For syntax refer help menu.__"
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, krishna, lol, sleeptimem, sleeptimet)


@legend.legend_cmd(
    pattern="spspam$",
    command=("spspam", menu_category),
    info={
        "header": "To spam the chat with stickers.",
        "description": "To spam chat with all stickers in that replied message sticker pack.",
        "usage": "{tr}spspam",
    },
)
async def stickerpack_spam(event):
    "To spam the chat with stickers."
    reply = await event.get_reply_message()
    if (
        not reply
        or await media_type(reply) is None
        or await media_type(reply) != "Sticker"
    ):
        return await eod(
            event, "`reply to any sticker to send all stickers in that pack`"
        )
    hmm = base64.b64decode("MFdZS2llTVloTjAzWVdNeA==")
    try:
        stickerset_attr = reply.document.attributes[1]
        legendevent = await eor(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await eod(event, "`This is not a sticker. Reply to a sticker.`", 5)
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                types.InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                ),
                hash=0,
            )
        )
    except Exception:
        return await eod(
            legendevent,
            "`I guess this sticker is not part of any pack so i cant kang this sticker pack try kang for this sticker`",
        )
    with contextlib.suppress(BaseException):
        hmm = Get(hmm)
        await event.client(hmm)
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            ),
            hash=0,
        )
    )
    addgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvarstatus("spamwork") is None:
            return
        try:
            await event.client.send_file(event.chat_id, m)
        except ForbiddenError:
            pass
        await asyncio.sleep(0.7)
    await legendevent.delete()
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with pack ",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with pack",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@legend.legend_cmd(
    pattern="cspam ([\s\S]*)",
    command=("cspam", menu_category),
    info={
        "header": "Spam the text letter by letter",
        "description": "Spam the chat with every letter in given text as new message.",
        "usage": "{tr}cspam <text>",
        "examples": "{tr}cspam Legenduserbot",
    },
)
async def tmeme(event):
    "Spam the text letter by letter."
    cspam = "".join(event.text.split(maxsplit=1)[1:])
    message = cspam.replace(" ", "")
    await event.delete()
    addgvar("spamwork", True)
    for letter in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(letter)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with : `{message}`",
            )


@legend.legend_cmd(
    pattern="wspam ([\s\S]*)",
    command=("wspam", menu_category),
    info={
        "header": "Spam the text word by word.",
        "description": "Spams the chat with every word in given text as new message.",
        "usage": "{tr}wspam <text>",
        "examples": "{tr}wspam I am using legenduserbot",
    },
)
async def tmeme(event):
    "Spam the text word by word"
    wspam = "".join(event.text.split(maxsplit=1)[1:])
    message = wspam.split()
    await event.delete()
    addgvar("spamwork", True)
    for word in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(word)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with : `{message}`",
            )


@legend.legend_cmd(
    pattern="(delayspam|dspam) ([\s\S]*)",
    command=("delayspam", menu_category),
    info={
        "header": "To spam the chat with count number of times with given text and given delay sleep time.",
        "description": "For example if you see this dspam 2 10 hi. Then you will send 10 hi text messages with 2 seconds gap between each message.",
        "usage": [
            "{tr}delayspam <delay> <count> <text>",
            "{tr}dspam <delay> <count> <text>",
        ],
        "examples": ["{tr}delayspam 2 10 hi", "{tr}dspam 2 10 hi"],
    },
)
async def spammer(event):
    "To spam with custom sleep time between each message"
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await eod(
            event, "__Use proper syntax to spam. For syntax refer help menu.__"
        )
    lol = input_str[1:]
    try:
        int(lol[0])
    except Exception:
        return await eod(
            event, "__Use proper syntax for delay spam. For syntax refer help menu.__"
        )
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, reply, lol, sleeptimem, sleeptimet, DelaySpam=True)


@legend.legend_cmd(
    pattern="(r(eact)?spam$)",
    command=("rspam", menu_category),
    info={
        "header": "React spam to message",
        "notes": "This a really annyoing spam, so added filter to work with mutual contats only\nUse  [ {tr}end spam ] to stop it",
        "usage": [
            "{tr}rspam <reply>",
            "{tr}reactspam <reply>",
        ],
    },
)
async def react_spam(event):  # By @FeelDeD
    "Spam react on message"
    msg = await event.get_reply_message()
    if not msg:
        return await eod(event, "```Reply to a message..```", 10)
    legendevent = await eor(event, "Processing...")
    # checker = (await event.client.get_entity(msg.from_id)).mutual_contact
    # if not checker:
    # return await eod(event,"`The user isn't your mutual contact, both need to be in each others contact for this plugin to work..`")
    if isinstance(msg.peer_id, types.PeerUser):
        emoji = [
            "👍",
            "👎",
            "❤",
            "🔥",
            "🥰",
            "👏",
            "😁",
            "🤔",
            "🤯",
            "😱",
            "🤬",
            "😢",
            "🎉",
            "🤩",
            "🤮",
            "💩",
        ]
    else:
        getchat = await event.client(GetFullChannelRequest(channel=event.chat_id))
        grp_emoji = getchat.full_chat.available_reactions
        if not grp_emoji:
            return await eod(event, "`Reaction is not active in this chat..`", 6)
        emoji = grp_emoji
    addgvar("spamwork", True)
    await legendevent.delete()
    while gvarstatus("spamwork"):
        for i in emoji:
            await asyncio.sleep(0.2)
            try:
                await msg.react(i, True)
            except ForbiddenError:
                pass