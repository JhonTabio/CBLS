from typing import Dict, List
import attrs
import enum
from lsprotocol.types import (
    SemanticTokenModifiers,
    SemanticTokenTypes)
from pygls.server import LanguageServer

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

KEYWORDS = [
    "if", 
    "while", 
    "return", 
    "for", 
    "def", 
    "class"
]

class CraftBlockLanguageServer(LanguageServer):
    """
        CraftBlockScript Language Server

        Currently able to highlight keywords and detect '#' tokens
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tokens: Dict[str, List[Token]] = {}
    
