# Urban Dictionary for legenduserbot by @mrconfused

from Legendbot import legend

from ..core.logger import logging
from ..core.managers import eod, eor
from ..helpers import AioHttp
from ..helpers.utils import _format

LOGS = logging.getLogger(__name__)
menu_category = "utils"


@legend.legend_cmd(
    pattern="ud ([\s\S]*)",
    command=("ud", menu_category),
    info={
        "header": "To fetch meaning of the given word from urban dictionary.",
        "usage": "{tr}ud <word>",
    },
)
async def _(event):
    "To fetch meaning of the given word from urban dictionary."
    word = event.pattern_match.group(1)
    try:
        response = await AioHttp().get_json(
            f"http://api.urbandictionary.com/v0/define?term={word}",
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        result = f"**Text: {_format.replacetext(word)}**\n**Meaning:**\n`{_format.replacetext(definition)}`\n\n**Example:**\n`{_format.replacetext(example)}`"
        await eor(event, result)
    except IndexError:
        await eod(
            event,
            text="`Sorry pal, we couldn't find meaning for the word you were looking for.`",
            time=10,
        )
    except Exception as e:
        await eod(event, text="`The Urban Dictionary API could not be reached`")
        LOGS.info(e)


@legend.legend_cmd(
    pattern="meaning ([\s\S]*)",
    command=("meaning", menu_category),
    info={
        "header": "To fetch meaning of the given word from dictionary.",
        "usage": "{tr}meaning <word>",
    },
)
async def _(event):
    "To fetch meaning of the given word from dictionary."
    word = event.pattern_match.group(1)
    try:
        ft = f"<b>Search Query: </b><code>{word.title()}</code>\n\n"
        response = await AioHttp().get_json(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
        )
        if "message" not in response:
            result = response[0]
            if "phonetic" in result:
                if phonetic := result["phonetic"]:
                    ft += f"<b>Phonetic: </b>\n<code>{phonetic}</code>\n\n"
            meanings = result["meanings"]
            synonyms = []
            antonyms = []
            for content in meanings:
                ft += f"<u><b>Meaning ({content['partOfSpeech']}):</b></u>\n"
                for count, text in enumerate(content["definitions"], 1):
                    ft += f"<b>{count}.</b> {text['definition']}\n"
                if content["synonyms"]:
                    synonyms.extend(content["synonyms"])
                if content["antonyms"]:
                    antonyms.extend(content["antonyms"])
                ft += "\n"
            if synonyms:
                ft += f"<b>Synonyms: </b><code>{', '.join(synonyms)}</code>\n"
            if antonyms:
                ft += f"<b>Antonyms: </b><code>{', '.join(antonyms)}</code>\n"
        else:
            ft += "`Sorry pal, we couldn't find Meaning for the word you were looking for.`"
        await eor(event, ft, parse_mode="html")
    except Exception as e:
        await eod(event, text="`The Dictionary API could not be reached`")
        LOGS.info(e)
