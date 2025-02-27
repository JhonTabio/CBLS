from ply.lex import lex

class CBLex(object):
    # Reserved Keywords
    reserved = {"dir", "desc", "import"}
    
    # Recognized tokens
    tokens = ["ID", "COMMENT", "NEWLINE"]
    
    # Add CAPS Keywords to our token list
    tokens = tokens + [r.upper() for r in reserved]
    
    t_ignore = '\r'
    
    # General token
    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = t.value.upper() if t.value in self.reserved else "ID"
        return t
    
    # Comment tokent
    def t_COMMENT(self, t):
        r"\#.+"
        return t
    
    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t
    
    # Unknown tokens
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' was skipped at {t.lexer.lineno}")
        t.lexer.skip(1)
    
    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # Build the lexer
    def build(self, **kwargs):
        # Uses reflections to interpret this file
        self.lexer = lex(module=self, **kwargs)

    def test(self, string):
        self.lexer.input(string)

        while True:
             token = self.lexer.token()
             if not token:
                 break

             print(token)
