import ply.yacc as yacc

class CBDiagnostic(object):
    def __init__(self, token, col, state, expected, message=None):
        self.token = token
        self.lineno = token.lineno
        self.col = col
        self.state = state
        self.message = f"Syntax error at line {token.lineno - 1} column {col - 1}. Unexpected {token.type} symbol {repr(token.value)} in state {state}. Expected {expected}" if message is None else message
        self.label = ""

    def __str__(self):
        return self.message + "\n" + self.label

class CBParse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.file_params = ["scale"]

        self.data = None
        self.diagnostics: list[CBDiagnostic] = []

    ### Parser rules
    ## File type rules -- Top level rules
    # .cbscript files
    def p_cbscript(self, p):
        """cbscript : script"""
        p[0] = ("cbscript", p[1])

    #def p_cblib(self, p):
        #"""cblib : lib"""
        #p[0] = ("cblib", p[1])

    ## Program type rules
    # Script rules
    def p_script(self, p):
        """script : dir optdesc file_params sections"""
        p[0] = {
            "DIR": p[1],
            "DESC": p[2]
        }

    # Dir rules
    def p_dir(self, p):
        """dir : DIR string newlines"""
        p[0] = p[2]

    def p_dir_error(self, p):
        """dir : DIR error newlines"""
        p[0] = "No output directroy"
        self.diagnostics[-1].label = "Expected a string for dir"
        self.parser.errok()

    # Desc rules
    def p_optdesc(self, p):
        """optdesc : DESC string newlines
                    | empty"""
        if len(p) < 4:
            p[0] = "No Description"
        else:
            p[0] = p[2]

    def p_optdesc_error(self, p):
        """optdesc : DESC error newlines"""
        p[0] = "No Description"
        self.diagnostics[-1].label = "Expected a string for desc"
        self.parser.errok()

    # File param rules
    def p_file_params(self, p):
        """file_params : file_param file_params optnewlines
                        | empty"""
        if len(p) > 2:
            n, v = p[1]
            p[2][n] = v
            p[0] = p[2]
        else:
            p[0] = {}

    def p_file_param(self, p):
        """file_param : ID int newlines"""
        if p[1] not in self.file_params:
            print(f"File param error: Unknown parameter '{p[1]}' at line {p.lineno(1)}")
        p[0] = (p[1], int(p[2]))

    def p_file_param_error(self, p):
        """file_param : ID error newlines"""
        if p[1] not in self.file_params:
            print(f"File param error: Unknown parameter '{p[1]}' at line {p.lineno(1)}")
        p[0] = (p[1], int(1000))
        self.parser.errok()

    ## Section rules
    def p_sections(self, p):
        """sections : section sections optnewlines
                    | empty"""

    # Section rule
    def p_section(self, p):
        """section : reset_section
                    | clock_section"""
        p[0] = p[1]

    # Reset rule - Entry point
    def p_reset_section(self, p):
        """reset_section : RESET newlines code_blocks END newlines"""
        pass

    def p_reset_section_error(self, p):
        """reset_section : RESET error END newlines"""
        self.parser.errok()
        pass

    # Clock rule - Update point
    def p_clock_section(self, p):
        """clock_section : CLOCK ID newlines code_blocks END newlines"""

    def p_clock_section_error(self, p):
        """clock_section : CLOCK error END newlines"""
        self.parser.errok()

    ## Code block rules
    def p_code_blocks(self, p):
        """code_blocks : code_block code_blocks optnewlines
                        | empty"""

    # Code block rule
    def p_code_block(self, p):
        """code_block : COMMAND optnewlines"""

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

    # Empty rule
    def p_empty(self, _):
        """empty :"""
        pass

    # Error catch-all
    def p_error(self, p):
        if p is None:
            print("Syntax error: unexpected End of File")
        else:
            state = self.parser.state
            expected = [token for token in self.parser.action[state].keys() if not token == "error"]
            self.diagnostics.append(CBDiagnostic(p, self.lexer.find_column(self.data, p), self.parser.state, expected))
            print(self.diagnostics[-1].message)

            # Handle 'dir' not first line
            if self.parser.state == 0: # Initial state, meaning first error we've ran into (Anything but 'dir')
                skip = 0 # Next parsing pass we skip n amount of error tokens
                while True:
                    token = self.parser.token()
                    if not token: # EOF
                        return # TODO: Handle never finding 'dir' token
                    elif token.type == "DIR":
                        break
                    skip += 1

                self.parser.restart() # Don't really think a reset is needed knowing this fires at state 0
                self.parser.errok()

                p.lexer.input(p.lexer.lexdata) # Reset lexer tokens
                p.lexer.lineno = 1 # Reset lexer line number
                for _ in range(skip + 1): # Skip n + 1 to include the first error token we missed
                    token = self.parser.token()
            else:
                pass
                #self.parser.token() # Skip errorneous token

    ### Parser Functions
    def parse(self, data, debug=0):
        self.lexer.lineno = 1 # Reset lexer every parse

        self.data = data
        #return self.parser.parse(data, debug=debug, tracking=True)
        ret =  self.parser.parse(data, debug=debug, tracking=True)
        for i, d in enumerate(self.diagnostics):
            print(f"[{i}]: {d}\n")
        return ret
