import attrs
import enum
from typing import List

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
    "command",
    "comment",
    "function",
    "keyword",
    "number",
    "operator",
    "parameter",
    "string",
    "type",
    "variable"
]

TOKEN_MAPPING = {
    # Variables and Identifiers
    "ID": "variable",
    "FUNCTIONID": "function",

    # String Literals
    "STRING": "string",

    # Comments
    "COMMENT": "comment",

    # Numbers
    "DECIMAL": "number",
    "FLOAT": "number",
    "HEX": "number",
    "BINARY": "number",
    "JSON": "number",

    # Arithmetic Operators
    "PLUS": "operator",
    "MINUS": "operator",
    "TIMES": "operator",
    "DIVIDE": "operator",
    "MODULO": "operator",
    "POWER": "operator",
    "PLUSPLUS": "operator",
    "MINUSMINUS": "operator",

    # Assignment Operators
    "EQUALS": "operator",
    "MINUS_EQUALS": "operator",
    "MODULO_EQUALS": "operator",
    "PLUS_EQUALS": "operator",
    "TIMES_EQUALS": "operator",

    # General Syntax Tokens
    "ATID": "type",
    "COMMAND": "command",
    "COLON": "operator",
    "DOLLAR": "operator",
    "DOT": "operator",
    "COMMA": "operator",
    "SEMICOLON": "operator",
    "TILDE": "operator",
    "TILDE_EMPTY": "operator",
    "REF": "operator",
    "NOT": "operator",

    # Data Types
    "array": "type",
    "block": "type",
    "block_data": "type",
    "block_tag": "type",
    "entity": "type",
    "entity_tag": "type",
    "item_tag": "type",
    "predicate": "type",
}
