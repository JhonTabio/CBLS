import ply.yacc as yacc

class CBParse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

        self.data = None

    ### Parser rules
    ## File type rules -- Top level rules
    # .cbscript files
    def p_cbscript(self, p):
        """cbscript : script"""
        p[0] = ("cbscript", p[1])

    ## Error handling rule for unexpected tokens before `DIR`
    def p_unexpected_start(self, p):
        """cbscript : generic script"""
        p[0] = ("cbscript", p[2])
        print("Syntax error: 'DIR' should be the first token in the file.")

    #def p_cblib(self, p):
        #"""cblib : lib"""
        #p[0] = ("cblib", p[1])

    ## Program type rules
    # Script rules
    def p_script(self, p):
        """script : DIR ID newlines DESC ID optnewlines"""
        p[0] = {
            "DIR": p[2],
            "DESC": p[5]
        }

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
    def p_newlines(self, p):
        """newlines : newlines NEWLINE
                    | NEWLINE"""
        p[0] = None

    def p_optnewlines(self, p):
        """optnewlines : newlines
                        | empty"""
        pass

    def p_generic(self, p):
        """generic : ID
                    | newlines
                    | number"""
        pass

    def p_empty(self, p):
        """empty :"""
        pass

    # Error catch-all
    def p_error(self, p):
        if p is None:
            print("Syntax error: unexpected End of File")
        else:
            print(f"Syntax error at line {p.lineno} column {self.lexer.find_column(self.data, p)}. Unexpected {p.type}  symbol {repr(p.value)} in state {self.parser.state}")

    ### Parser Functions
    def parse(self, data, debug=0):
        self.lexer.lineno = 1 # Reset lexer every parse

        self.data = data
        return self.parser.parse(data, debug=debug, tracking=True)
