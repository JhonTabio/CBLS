import enum

class TokenModifier(enum.IntFlag):
    deprecated = enum.auto()
    readonly = enum.auto()
    defaultLibrary = enum.auto()
    definition = enum.auto()

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
    "PLUS_PLUS": "operator",
    "MINUS_MINUS": "operator",

    # Assignment Operators
    "EQUALS": "operator",
    "MINUS_EQUALS": "operator",
    "MODULO_EQUALS": "operator",
    "PLUS_EQUALS": "operator",
    "TIMES_EQUALS": "operator",

    # Comparison Operators
    "EQUALS_EQUALS": "operator",
    "GREATER": "operator",
    "GREATER_EQUALS": "operator",
    "LESS": "operator",
    "LESS_EQUALS": "operator",

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
    "NEGATION": "operator",

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
