import attrs
import enum
import re
from typing import List, Optional

class TokenModifier(enum.IntFlag):
    deprecated = enum.auto()
    readonly = enum.auto()
    defaultLibrary = enum.auto()
    definition = enum.auto()

@attrs.define
class Token:
    """
        Tokens are sent to the client as a long list of numbers, each group of 5 numbers describe
        a single token.
        
            - The first 3 numbers describe the token's line number, character index and length,
              **relative to the start of the previous token**
            - Thr 4th number describes a token's type
            - The 5th number specifies zero or more modifiers to apply to a token
    """
    line: int       # Token's line number
    offset: int     # Character index
    text: str       # Instead of length, we opt for the text itself

    token_type: str = "" # Token type
    token_modifiers: List[TokenModifier] = attrs.field(factory=list) # Token Modifier


TOKEN_TYPES = [
    "function",
    "keyword",
    "operator",
    "parameter",
    "type",
    "variable"
]

# Taken from CBScript source code
KEYWORDS = [
    "for", "dir", "desc", "in", "end", "not", "and", "or", "to", "by", "import",
    "name", "with", "macros", "at", "as", "on", "facing", "rotated", "align", "here",
    "the_end", "the_nether", "overworld", "move", "create", "tell", "title", "subtitle",
    "actionbar", "reset", "clock", "function", "if", "unless", "then", "do", "else", "switch",
    "case", "default", "return", "while", "macro", "entity", "block", "block_data", "block_tag",
    "entity_tag", "item_tag", "define", "array", "remove", "success", "result", "shaped", "recipe",
    "keys", "eyes", "feet",	"advancement", "loot_table", "predicate", "item_modifier", "push", "pop",
    "true", "false"
]

# First character *must* be a letter/underscore
# The remaining can be letters, numbers or underscores
IDENTIFIERS = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# Symbol characters
SYMBOLS = re.compile(r"[\+\-\=\,\*/\(\)\{\}]")

# Space
SPACE = re.compile(r"\s+")

def is_keyword(token: Optional[Token]) -> bool:
    return token is not None and token.text in KEYWORDS and token.token_type == "keyword"
