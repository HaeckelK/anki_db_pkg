import random
import string
import time
import re
from hashlib import sha1
from typing import Iterable, Iterator, List, Optional, Union

# anki/pylib/anki/utils.py
def guid64() -> str:
    "Return a base91-encoded 64bit random number."
    return base91(random.randint(0, 2 ** 64 - 1))

# anki/pylib/anki/utils.py
def base62(num: int, extra: str = "") -> str:
    s = string
    table = s.ascii_letters + s.digits + extra
    buf = ""
    while num:
        num, i = divmod(num, len(table))
        buf = table[i] + buf
    return buf


_base91_extra_chars = "!#$%&()*+,-./:;<=>?@[]^_`{|}~"

# anki/pylib/anki/utils.py
def base91(num: int) -> str:
    # all printable characters minus quotes, backslash and separators
    return base62(num, _base91_extra_chars)

def intTime(scale: int = 1) -> int:
    "The time in integer seconds. Pass scale=1000 to get milliseconds."
    return int(time.time() * scale)

# Checksums
##############################################################################

def checksum(data: Union[bytes, str]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return sha1(data).hexdigest()


def fieldChecksum(data: str) -> int:
    # 32 bit unsigned number from first 8 digits of sha1 hash
    return int(checksum(stripHTMLMedia(data).encode("utf-8"))[:8], 16)

# Fields
##############################################################################


def joinFields(list: List[str]) -> str:
    return "\x1f".join(list)


def splitFields(string: str) -> List[str]:
    return string.split("\x1f")

# HTML
##############################################################################
reComment = re.compile("(?s)<!--.*?-->")
reStyle = re.compile("(?si)<style.*?>.*?</style>")
reScript = re.compile("(?si)<script.*?>.*?</script>")
reTag = re.compile("(?s)<.*?>")
reEnts = re.compile(r"&#?\w+;")
reMedia = re.compile("(?i)<img[^>]+src=[\"']?([^\"'>]+)[\"']?[^>]*>")

def stripHTMLMedia(s: str) -> str:
    "Strip HTML but keep media filenames"
    s = reMedia.sub(" \\1 ", s)
    return stripHTML(s)

def stripHTML(s: str) -> str:
    s = reComment.sub("", s)
    s = reStyle.sub("", s)
    s = reScript.sub("", s)
    s = reTag.sub("", s)
    s = entsToTxt(s)
    return s

def entsToTxt(html: str) -> str:
    # entitydefs defines nbsp as \xa0 instead of a standard space, so we
    # replace it first
    html = html.replace("&nbsp;", " ")

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return reEnts.sub(fixup, html)
