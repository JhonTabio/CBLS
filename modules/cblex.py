from ply.lex import lex

class CBLex(object):
    # Build the lexer - Build once!
    def __init__(self, **kwargs):
        # Reserved Keywords
        self.reserved = {
            # General keywords
            "case", "default", "define", "desc", "dir", "do", "end", "for",
            "function", "if", "import", "in", "name", "return",
            "switch", "then", "unless", "while", "with",

            # Boolean keywords
            "false", "true",

            # Section keywords
            "clock", "macros", "reset",

            # World space alignment keywords
            "align", "as", "at", "eyes", "facing", "feet", "here",
            "move", "overworld", "rotated", "the_end", "the_nether",

            # Command keywords
            "actionbar", "create", "tell", "title", "subtitle",

            # Data types
            "array", "block", "block_data", "block_tag", "entity", "entity_tag",
            "item_tag", "predicate"

            # Stack operations
            "pop", "push"

        }

        # Recognized tokens
        self.tokens = [
            # General tokens
            "COMMAND", "COMMENT", "ID", "NEWLINE", "STRING", "WHITESPACE",

            # Number tokens
            "BINARY", "DECIMAL", "FLOAT", "HEX",

            # Arithmetic tokens
            "DIVIDE", "MINUS", "MINUSMINUS", "MODULO", 
            "POWER", "PLUS", "PLUSPLUS", "TIMES",]

        # Add CAPS Keywords to our token list
        self.tokens = self.tokens + [r.upper() for r in self.reserved]

        ### Ignored Tokens
        self.t_ignore = '\r'

        ### Simple tokens
        ## Arithmetic Operator tokens
        self.t_PLUS = r"\+"
        self.t_PLUSPLUS = r"\+\+"
        self.t_MINUS = r"-"
        self.t_MINUSMINUS = r"--"
        self.t_TIMES = r"\*"
        self.t_DIVIDE = r"/"
        self.t_MODULO = r"%"
        self.t_POWER = r"\^"

        ## Numerical tokens
        self.t_DECIMAL = r"\d+"
        self.t_FLOAT = r"\d+\.\d+"

        # Uses reflections to interpret this file
        self.lexer = lex(module=self, **kwargs)

    ### Complex tokens with action code
    ## Standard tokens
    # General token
    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        # If a keyword, categorize as such else ID
        t.type = t.value.upper() if t.value in self.reserved else "ID"
        return t
    
    def t_COMMAND(self, t):
        r"(?m:^\s*\/.+)"
        t.lexer.lineno += t.value.count('\n')
        t.value = t.value.strip()
        return t

    # String token
    def t_STRING(self, t):
        r"(\"((\\.)|[^\"\n])*\")|('((\\.)|[^'\n])*')"
        return t
    
    # Comment token
    def t_COMMENT(self, _):
        r"\#.+"
        pass
    
    # Newline token
    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t

    # Space/Tab token
    def t_WHITESPACE(self, _):
        r"[ \t]"
        pass
    
    # Unknown tokens
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' was skipped at {t.lexer.lineno}")
        t.lexer.skip(1)

    ## Numerical tokens
    # Binary token
    def t_BINARY(self, t):
        r"0b[01]+"
        # Retrieve decimal value from binary
        t.value = str(int(t.value, 2))
        return t

    # Hexadecimal token
    def t_HEX(self, t):
        r"0x[a-fA-F0-9]+"
        # Retrieve decimal value from hex
        t.value = str(int(t.value, 16))
        return t
    
    ### Lexer functions
    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # Test the lexer
    def test(self, string):
        self.lexer.input(string)

        while True:
             token = self.lexer.token()

             if not token:
                 break

             print(token)

    def reset(self):
        self.lexer.lineno = 1
