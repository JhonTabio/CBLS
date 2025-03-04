import ply.yacc as yacc

class CBDiagnostic(object):
    def __init__(self, token, col, state, message=None):
        self.token = token
        self.lineno = token.lineno
        self.col = col
        self.state = state
        self.message = f"Syntax error at line {token.lineno} column {col}. Unexpected {token.type} symbol {repr(token.value)} in state {state}" if message is None else message
        self.label = ""

class CBParse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

        self.data = None
        self.diagnostics: list[CBDiagnostic] = []

    ### Parser rules
    ## File type rules -- Top level rules
    # .cbscript files
    def p_cbscript(self, p):
        """cbscript : script"""
        p[0] = ("cbscript", p[1])

    ## Error handling rule for unexpected tokens before `DIR`
    def p_unexpected_start(self, p):
        """cbscript : generic script"""
        p[0] = ("cbscript", p[2], "'dir' should be the first keyword in the file")

    #def p_cblib(self, p):
        #"""cblib : lib"""
        #p[0] = ("cblib", p[1])

    ## Program type rules
    # Script rules
    def p_script(self, p):
        """script : dir optdesc"""
        p[0] = {
            "DIR": p[1],
            "DESC": p[2]
        }

    def p_dir(self, p):
        """dir : DIR string optnewlines"""
        p[0] = p[2]

    def p_dir_error(self, p):
        """dir : DIR error optnewlines"""
        p[0] = "No output directroy"
        self.diagnostics[-1].label = "Expected a string"

    def p_optdesc(self, p):
        """optdesc : DESC string optnewlines
                    | empty"""
        if len(p) < 4:
            p[0] = "No Description"
        else:
            p[0] = p[2]

    def p_optdesc_error(self, p):
        """optdesc : DESC error optnewlines"""
        p[0] = "No Description"
        self.diagnostics[-1].label = "Expected a string"

    ## String rules
    # String rule
    def p_string(self, p):
        """string : STRING"""
        p[0] = p[1][1:-1]

    ## Number rules
    # Number rule
    def p_number(self, p):
        """number : int
                    | float"""
        p[0] = p[1]

    # Integer rules
    def p_int(self, p):
        """int : BINARY
                | DECIMAL
                | HEX"""
        p[0] = p[1]

    # Negative Integer rules
    def p_int_negative(self, p):
        """int : MINUS BINARY
                | MINUS DECIMAL
                | MINUS HEX"""
        p[0] = str(-int(p[2]))

    # Float rules
    def p_float(self, p):
        """float : FLOAT"""
        p[0] = p[1]

    # Negative Float rules
    def p_float_negative(self, p):
        """float : MINUS FLOAT"""
        p[0] = str(-float(p[2]))

    ## MISC rules
    # Newline rule
    def p_newlines(self, p):
        """newlines : newlines NEWLINE
                    | NEWLINE"""
        p[0] = None

    # Optional newline rule
    def p_optnewlines(self, _):
        """optnewlines : newlines
                        | empty"""
        pass

    # Standalone token rule
    def p_generic(self, _):
        """generic : ID
                    | newlines
                    | number"""
        pass

    # Empty rule
    def p_empty(self, _):
        """empty :"""
        pass

    # Error catch-all
    def p_error(self, p):
        if p is None:
            print("Syntax error: unexpected End of File")
        else:
            self.diagnostics.append(CBDiagnostic(p, self.lexer.find_column(self.data, p), self.parser.state))
            print(self.diagnostics[-1].message)
            #print(f"Syntax error at line {p.lineno} column {self.lexer.find_column(self.data, p)}. Unexpected {p.type} symbol {repr(p.value)} in state {self.parser.state}")

    ### Parser Functions
    def parse(self, data, debug=0):
        self.lexer.lineno = 1 # Reset lexer every parse

        self.data = data
        return self.parser.parse(data, debug=debug, tracking=True)
