from ply.lex import lex

class CBLex(object):
    # Reserved Keywords
    reserved = {"dir", "desc", "import"}
    
    # Recognized tokens
    tokens = ["BINARY", "COMMENT", "DECIMAL", "DIVIDE", "FLOAT", "HEX", "ID", "MINUS", "MINUSMINUS", "MODULO", "NEWLINE", "POWER", "PLUS", "PLUSPLUS", "TIMES", "WHITESPACE"]
    
    # Add CAPS Keywords to our token list
    tokens = tokens + [r.upper() for r in reserved]
    
    ### Ignored Tokens
    t_ignore = '\r'

    ### Simple tokens
    ## Arithmetic Operator tokens
    t_PLUS = r"\+"
    t_PLUSPLUS = r"\+\+"
    t_MINUS = r"-"
    t_MINUSMINUS = r"--"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_MODULO = r"%"
    t_POWER = r"\^"

    ## Numerical tokens
    t_DECIMAL = r"\d+"
    t_FLOAT = r"\d+\.\d+"
    
    ### Complex tokens with action code
    ## Standard tokens
    # General token
    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        # If a keyword, categorize as such else ID
        t.type = t.value.upper() if t.value in self.reserved else "ID"
        return t
    
    # Comment token
    def t_COMMENT(self, t):
        r"\#.+"
        return t
    
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
    
    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # Build the lexer - Build once!
    def build(self, **kwargs):
        # Uses reflections to interpret this file
        self.lexer = lex(module=self, **kwargs)

    # Test the lexer
    def test(self, string):
        self.lexer.input(string)

        while True:
             token = self.lexer.token()
             if not token:
                 break

             print(token)
