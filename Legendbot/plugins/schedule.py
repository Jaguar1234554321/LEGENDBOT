from asyncio import sleep

from Legendbot import legend

menu_category = "utils"


@legend.legend_cmd(
    pattern="schd (\d*) ([\s\S]*)",
    command=("schd", menu_category),
    info={
        "header": "To schedule a message after given time(in seconds).",
        "usage": "{tr}schd <time_in_seconds>  <message to send>",
        "examples": "{tr}schd 120 hello",
    },
)
async def _(event):
    "To schedule a message after given time"
    lol = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = lol[1]
    ttl = int(lol[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
