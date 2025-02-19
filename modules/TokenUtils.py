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
    "command",
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

# Able to catch multiple command lines
# Captures all leading whitespace
# First character *must* be a '/'
COMMANDS = re.compile(r"^\s*/.+", re.MULTILINE)

# Symbol characters
#SYMBOLS = re.compile(r"[\+\-\=\,\*/\(\)\{\}]")

# Arithmetic Operators
SYMBOL_PLUS = re.compile(r"\+")
SYMBOL_MINUS = re.compile(r"-")
SYMBOL_TIMES = re.compile(r"\*")
SYMBOL_DIVIDE = re.compile(r"/")
SYMBOL_MODULO = re.compile(r"%")
SYMBOL_POWER = re.compile(r"\^")

SYMBOL_PLUS_PLUS = re.compile(r"\+\+")
SYMBOL_MINUS_MINUS = re.compile(r"--")

# Comparison Operators
SYMBOL_EQUAL = re.compile(r"==")
#SYMBOL_NOT_EQUAL = re.compile(r"!=")
SYMBOL_LESS_THAN = re.compile(r"<")
SYMBOL_GREATER_THAN = re.compile(r">")
SYMBOL_LESS_EQUAL = re.compile(r"<=")
SYMBOL_GREATER_EQUAL = re.compile(r">=")

# Logical Operators
#SYMBOL_AND = re.compile(r"&&")
#SYMBOL_OR = re.compile(r"\|\|")
SYMBOL_NOT = re.compile(r"!")

# Assignment Operators
SYMBOL_ASSIGN = re.compile(r"=")
SYMBOL_PLUS_ASSIGN = re.compile(r"\+=")
SYMBOL_MINUS_ASSIGN = re.compile(r"-=")
SYMBOL_TIMES_ASSIGN = re.compile(r"\*=")
SYMBOL_DIVIDE_ASSIGN = re.compile(r"/=")
SYMBOL_MODULO_ASSIGN = re.compile(r"%=")

# Bitwise Operators
#SYMBOL_BITWISE_AND = re.compile(r"&")
#SYMBOL_BITWISE_OR = re.compile(r"\|")
#SYMBOL_BITWISE_XOR = re.compile(r"\^")
#SYMBOL_BITWISE_NOT = re.compile(r"~")
#SYMBOL_BITWISE_SHIFT_LEFT = re.compile(r"<<")
#SYMBOL_BITWISE_SHIFT_RIGHT = re.compile(r">>")

# Delimiters & Separators
#SYMBOL_COMMA = re.compile(r",")
SYMBOL_SEMICOLON = re.compile(r";")
SYMBOL_COLON = re.compile(r":")
SYMBOL_DOT = re.compile(r"\.")

# Parentheses, Brackets, and Braces
SYMBOL_LPAREN = re.compile(r"\(")   # Left Parenthesis
SYMBOL_RPAREN = re.compile(r"\)")   # Right Parenthesis
SYMBOL_LBRACK = re.compile(r"\[")   # Left Bracket
SYMBOL_RBRACK = re.compile(r"\]")   # Right Bracket
SYMBOL_LCURLY = re.compile(r"\{")   # Left Curly Brace
SYMBOL_RCURLY = re.compile(r"\}")   # Right Curly Brace

# Special Symbols
SYMBOL_DOLLAR = re.compile(r"\$")
#SYMBOL_AT = re.compile(r"@")
#SYMBOL_HASH = re.compile(r"#")
#SYMBOL_QUESTION = re.compile(r"\?")
#SYMBOL_BACKSLASH = re.compile(r"\\")
#SYMBOL_FORWARD_SLASH = re.compile(r"/")
#SYMBOL_UNDERSCORE = re.compile(r"_")

# Arrow Operators
#SYMBOL_ARROW_RIGHT = re.compile(r"->")
#SYMBOL_ARROW_LEFT = re.compile(r"<-")

# Numbers
FLOAT = re.compile(r"\d+\.\d+")
DECIMAL = re.compile(r"\d+")

# CBScript Related
SYMBOL_REF = re.compile(r"&")
SYMBOL_TILDE = re.compile(r"~")
SYMBOL_TILDE_EMPTY = re.compile(r"~[ \t]")

# Space + Tabs
SPACE = re.compile(r"[ \t]+")

# New line
NEW_LINE = re.compile(r"\n")

def is_keyword(token: Optional[Token]) -> bool:
    return token is not None and token.text in KEYWORDS and token.token_type == "keyword"
